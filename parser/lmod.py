import os
import re
import glob
import config
import pickle
import datetime
import subprocess
from lupa import LuaRuntime
import utils
from parser.common import extract_installer


def run_collect_data_script():
    try:
        result = subprocess.run(['python', 'collect_data.py'], check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        utils.append_log(f"Failed to run collect_data.py: {e}", config.main_log_file)
        print(f"Failed to run collect_data.py: {e}")
        return False


def process_modulepath(modulepaths, title, output_dir):
    # Run collect_data.py if data file doesn't exist
    collected_data = utils.ensure_data_collected()

    if collected_data:
        package_infos, latest_version_info, package_ref = extract_package_info(collected_data)
    else:
        package_infos, latest_version_info, package_ref = None, None, None

    return package_infos, latest_version_info, package_ref


def process_broken_symlinks():
    if not os.path.exists(config.broken_symlinks_file):
        print(f"No broken symlinks file found for date: {config.current_date}")
        return

    with open(config.broken_symlinks_file, 'r') as file:
        broken_symlinks = file.readlines()

    utils.append_file(config.broken_symlinks_file, f"\n\nls -lrtah <file not found>\n")
    utils.append_file(config.broken_symlinks_file, f"\nls -lrath <symlink target>\n\n")
    for symlink in broken_symlinks:
        symlink = symlink.strip()
        if symlink:
            result = subprocess.run(['ls', '-lrtah', symlink], capture_output=True, text=True)
            utils.append_file(config.broken_symlinks_file, result.stdout)
            utils.append_file(config.broken_symlinks_file, result.stderr)

            target = os.path.realpath(symlink)
            if target:
                result = subprocess.run(['ls', '-lrath', target], capture_output=True, text=True)
                utils.append_file(config.broken_symlinks_file, result.stdout)
                utils.append_file(config.broken_symlinks_file, result.stderr)


def extract_package_info(collected_data):
    """
    Extracts package information, latest version info, and categorises each package
    by its primary category from the collected data.

    Args:
        collected_data (dict): Dictionary containing `package_infos` and `latest_version_info`.

    Returns:
        tuple: A tuple containing:
            - package_infos (dict): Information about each package.
            - latest_version_info (dict): Latest version information for each package.
            - package_ref (dict): A dictionary mapping each package to its primary category.
    """
    package_infos = collected_data.get('package_infos', {})
    latest_version_info = collected_data.get('latest_version_info', {})

    package_ref = {}

    for key in latest_version_info.keys():
        categories = set()

        for arch in latest_version_info[key]:
            category, package = key.split('|')
            categories.add(category)

        if package not in package_ref:
            primary_category = next((cat for cat in categories if cat != "All"), "All")
            package_ref[package] = primary_category
        else:
            if package_ref[package] == "All":
                non_all_category = next((cat for cat in categories if cat != "All"), None)
                if non_all_category:
                    package_ref[package] = non_all_category

    return package_infos, latest_version_info, package_ref


def read_lua_file(lua_file_path):
    """
    Reads the content of a Lua file. Logs and records any errors.

    Args:
        lua_file_path (str): The path to the Lua file.

    Returns:
        str: The content of the Lua file if successful, or None if there was an error.
    """
    try:
        with open(lua_file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        log_message = f"{lua_file_path} not found.\n"
        print(log_message.strip())
        utils.append_file(config.broken_symlinks_file, log_message)
        return None
    except Exception as e:
        log_message = f"Error reading {lua_file_path}: {e}\n"
        print(log_message.strip())
        utils.append_file(config.broken_symlinks_file, log_message)
        return None


def setup_lua_runtime() -> LuaRuntime:
    lua = LuaRuntime(unpack_returned_tuples=True)

    try:
        lua.execute('''
        function help(msg) end
        function whatis(msg) end
        function prepend_path(var, value) end
        function append_path(var, value) end
        function setenv(var, value) _G.env_vars[var] = value end
        function unsetenv(var) end
        function load(module) end
        function unload(module) end
        function conflict(module) end
        function family(module) end
        function add_property(var, value) end
        function remove_property(var) end
        function isloaded(module) return false end
        function pathJoin(...) return table.concat({...}, "/") end

        setmetatable(_G, {
            __index = function(_, key)
                _G[key] = function(...) end
                return _G[key]
            end
        })

        _G.env_vars = {}
        ''')

        assert isinstance(lua, LuaRuntime), "Expected lua to be an instance of LuaRuntime"
        return lua
    except Exception as e:
        print(f"Error in Lua setup: {e}")
        return None


def execute_lua(lua, lua_content, lua_file_path):
    """
    Executes Lua content and logs errors if execution fails.

    Args:
        lua (LuaRuntime): An instance of LuaRuntime.
        lua_content (str): The Lua code to execute.
        lua_file_path (str): The path of the Lua file being processed (for logging purposes).

    Returns:
        bool: True if execution succeeds, None if it fails.
    """
    try:
        lua.execute(lua_content)
        return True
    except Exception as e:
        log_message = f"Error executing Lua content in {lua_file_path}: {e}\n"
        print(log_message.strip())
        utils.append_file(config.log_file_path, log_message)
        return None


def extract_patterns(lua_content):
    """Extracts data using regex patterns from Lua content."""
    patterns = {
        "help_info": re.compile(r'help\(\[\=\=\[(.*?)\]\=\=\]\)', re.DOTALL),
        "whatis_info": re.compile(r'whatis\(\[\=\=\[(.*?)\]\=\=\]\)', re.DOTALL),
        "loaded_modules": re.compile(r'load\("(.*?)"\)'),
        "env_vars": re.compile(r'setenv\("([^"]+)",\s*"([^"]+)"\)'),
        "root": re.compile(r'local root = "(.*?)"')
    }
    extracted_data = {key: pattern.findall(lua_content) for key, pattern in patterns.items()}
    extracted_data["root"] = extracted_data["root"][0] if extracted_data["root"] else None
    return extracted_data


def process_env_vars(env_vars, lua_globals):
    """Processes environment variables from Lua and merges them with Lua globals."""
    env_vars_dict = {key: lua_globals[key] for key in lua_globals.keys()}
    for var, value in env_vars:
        env_vars_dict[var] = value
    return env_vars_dict


def extract_module_info(lua_content, lua_globals):
    """Extracts and organizes module information from Lua content."""
    data = extract_patterns(lua_content)
    env_vars_dict = process_env_vars(data["env_vars"], lua_globals)
    package_suffix = next((key.split('EBROOT')[-1] for key in env_vars_dict if key.startswith('EBROOT')), '')

    eb_vars = {
        k.replace(package_suffix, ''): {
            'value': v,
            'var_name': k
        }
        for k, v in env_vars_dict.items() if k.startswith('EB')
    }

    return {
        "WhatIs Information": [info.strip() for info in data["whatis_info"]],
        "Loaded Modules": data["loaded_modules"],
        "Root": data["root"],
        "EB Variables": eb_vars,
        "EB Version": eb_vars.get('EBVERSION', {}).get('value', None)
    }


def log_module_info(module_info):
    """Logs module information to the configured log file."""
    utils.append_log(f"\nParsed: {config.lua_file_path}", config.log_file_path)
    for key, value in module_info.items():
        utils.append_log(f"\n{key}:", config.log_file_path)
        if isinstance(value, list):
            for item in value:
                utils.append_log(item, config.log_file_path)
        elif isinstance(value, dict):
            for var, val in value.items():
                utils.append_log(f"{var} = {val['value']} (variable: {val['var_name']})", config.log_file_path)
        else:
            utils.append_log(value, config.log_file_path)


def extract_lua_info(lua_file_path):
    """Extracts and returns module information from a Lua file."""
    lua_content = read_lua_file(lua_file_path)
    if not lua_content:
        return None, None, None

    lua = setup_lua_runtime()
    if not execute_lua(lua, lua_content, lua_file_path):
        return None, None, None

    module_info = extract_module_info(lua_content, lua.globals().env_vars)
    log_module_info(module_info)
    creation_date = datetime.datetime.fromtimestamp(os.path.getctime(lua_file_path)).strftime('%Y-%m-%d')
    installer = extract_installer(lua_file_path)
    return module_info, creation_date, installer


def gather_lua_paths_by_arch():
    """Gathers Lua file paths organized by architecture."""
    paths_by_arch = {arch: mp.replace('/all', '').split(':') for arch, mp in config.modulepaths.items()}
    extracted_paths_by_arch = {
        arch: [
            (file, '/'.join(file.split('/')[-3:]).replace('.lua', ''))
            for path in paths
            for file in glob.glob(os.path.join(path, '*/*/*.lua'))
        ]
        for arch, paths in paths_by_arch.items()
    }
    return extracted_paths_by_arch


def sort_paths(paths_by_arch):
    """Sorts Lua file paths for each architecture."""
    sorted_paths_by_arch = {
        arch: sorted(
            paths,
            key=lambda path: (
                path[1].split('/')[0].casefold(),
                path[1].split('/')[1].casefold(),
                [
                    (-int(x) if x.isdigit() else x.casefold())
                    for x in re.split('(\d+)', path[1].split('/')[2])
                ]
            )
        )
        for arch, paths in paths_by_arch.items()
    }
    return sorted_paths_by_arch


def process_paths_for_architecture(paths, arch, parser_module, latest_version_info, package_infos):
    """
    Processes Lua paths for a given architecture, extracting module information
    and updating the latest version and package information dictionaries.

    Args:
        paths (list): List of (lua_file_path, extracted_path) tuples for the architecture.
        arch (str): The architecture name (e.g., 'x86_64', 'arm64').
        parser_module (module): The parser module used to extract Lua information.
        latest_version_info (dict): Dictionary to store the latest version info by category and package.
        package_infos (dict): Dictionary to store package information by architecture.
    """
    for lua_file_path, extracted_path in paths:
        category, package, version = extracted_path.split('/')
        category = category.capitalize()

        # Initialize latest_version_info entry if not present
        if (category, package) not in latest_version_info:
            latest_version_info[(category, package)] = {}

        # Extract module information if not already processed for this architecture
        if arch not in latest_version_info[(category, package)]:
            module_info, creation_date, installer = parser_module.extract_lua_info(lua_file_path)
            if module_info is None:
                continue  # Skip if information could not be extracted

            latest_version_info[(category, package)][arch] = (module_info, creation_date, installer)

        # Update package information if this version is not yet recorded
        if (category, package, version) not in package_infos[arch]:
            package_infos[arch][(category, package, version)] = (lua_file_path, version)
