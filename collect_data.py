import os
import re
import glob
import pickle
import datetime
import subprocess
from lupa import LuaRuntime
import config

def write_log(log_file_path):
    with open(log_file_path, 'w') as log_file:
        log_file.write("")

def write_output(message):
    if message is None:
        message = ""
    with open(config.log_file_path, 'a') as f:
        f.write(message + '\n')
    print(message)

def append_file(filepath, content):
    with open(filepath, 'a') as file:
        file.write(content)

def process_broken_symlinks():
    if not os.path.exists(config.broken_symlinks_file):
        print(f"No broken symlinks file found for date: {current_date}")
        return

    with open(config.broken_symlinks_file, 'r') as file:
        broken_symlinks = file.readlines()

    append_file(config.broken_symlinks_file, f"\n\nls -lrtah <file not found>\n")
    append_file(config.broken_symlinks_file, f"\nls -lrath <symlink target>\n\n")
    for symlink in broken_symlinks:
        symlink = symlink.strip()
        if symlink:
            result = subprocess.run(['ls', '-lrtah', symlink], capture_output=True, text=True)
            append_file(config.broken_symlinks_file, result.stdout)
            append_file(config.broken_symlinks_file, result.stderr)

            target = os.path.realpath(symlink)
            if target:
                result = subprocess.run(['ls', '-lrath', target], capture_output=True, text=True)
                append_file(config.broken_symlinks_file, result.stdout)
                append_file(config.broken_symlinks_file, result.stderr)

def extract_lua_info(lua_file_path):
    try:
        with open(lua_file_path, 'r') as file:
            lua_content = file.read()
    except FileNotFoundError:
        log_message = f"{lua_file_path}\n"
        print(log_message.strip())
        append_file(config.broken_symlinks_file, log_message)
        return None, None, None
    except Exception as e:
        log_message = f"Error reading {lua_file_path}: {e}\n"
        print(log_message.strip())
        append_file(config.broken_symlinks_file, log_message)
        return None, None, None

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

        lua.execute(lua_content)
    except Exception as e:
        log_message = f"Error executing Lua content in {lua_file_path}: {e}\n"
        print(log_message.strip())
        append_file(log_file_path, log_message)
        return None, None, None

    help_pattern = re.compile(r'help\(\[\=\=\[(.*?)\]\=\=\]\)', re.DOTALL)
    whatis_pattern = re.compile(r'whatis\(\[\=\=\[(.*?)\]\=\=\]\)', re.DOTALL)
    load_pattern = re.compile(r'load\("(.*?)"\)')
    env_pattern = re.compile(r'setenv\("([^"]+)",\s*"([^"]+)"\)')
    root_pattern = re.compile(r'local root = "(.*?)"')

    help_info = help_pattern.findall(lua_content)
    whatis_info = whatis_pattern.findall(lua_content)
    loaded_modules = load_pattern.findall(lua_content)
    env_vars = env_pattern.findall(lua_content)

    root_match = root_pattern.search(lua_content)
    root = root_match.group(1) if root_match else None

    env_vars_lua = lua.globals().env_vars
    env_vars_dict = {key: env_vars_lua[key] for key in env_vars_lua.keys()}

    for var, value in env_vars:
        env_vars_dict[var] = value

    package_suffix = next((key.split('EBROOT')[-1] for key in env_vars_dict if key.startswith('EBROOT')), '')

    eb_vars = {
        k.replace(package_suffix, ''): {
            'value': v,
            'var_name': k
        }
        for k, v in env_vars_dict.items() if k.startswith('EB')
    }

    ebversion_var = eb_vars.get('EBVERSION', {}).get('value', None)

    module_info = {
        "WhatIs Information": [info.strip() for info in whatis_info],
        "Loaded Modules": loaded_modules,
        "Root": root,
        "EB Variables": eb_vars,
        "EB Version": ebversion_var
    }

    write_output(f"\nParsed: {lua_file_path}")
    for key, value in module_info.items():
        write_output(f"\n{key}:")
        if isinstance(value, list):
            for item in value:
                write_output(item)
        elif isinstance(value, dict):
            for var, val in value.items():
                if isinstance(val, dict):
                    write_output(f"{var} = {val['value']} (variable: {val['var_name']})")
                else:
                    write_output(f"{var} = {val}")
        else:
            write_output(value)

    creation_time = os.path.getctime(lua_file_path)
    creation_date = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d')

    installer = extract_installer(lua_file_path)

    return module_info, creation_date, installer

def extract_installer(file_path):
    try:
        result = subprocess.run(['ls', '-lrath', file_path], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.splitlines()
            for line in lines:
                parts = line.split()
                if len(parts) > 2:
                    user = parts[2]
                    if user.startswith('sa_'):
                        return user[3:]
    except Exception as e:
        write_output(f"Error extracting installer: {e}")
    return None

def save_collected_data(file_path, data):
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)

def collect_data():
    paths_by_arch = {arch: mp.replace('/all', '').split(':') for arch, mp in config.modulepaths.items()}
    extracted_paths_by_arch = {arch: [(file, '/'.join(file.split('/')[-3:]).replace('.lua', '')) for path in paths for file in glob.glob(os.path.join(path, '*/*/*.lua'))] for arch, paths in paths_by_arch.items()}
    sorted_paths_by_arch = {
        arch: sorted(
            paths,
            key=lambda path: (
                path[1].split('/')[0].casefold(),
                path[1].split('/')[1].casefold(),
                # Negate the numbers for reverse sorting
                [
                    (-int(x) if x.isdigit() else x.casefold()) 
                    for x in re.split('(\d+)', path[1].split('/')[2])
                ]
            )
        )
        for arch, paths in extracted_paths_by_arch.items()
    }

    package_infos = {arch: {} for arch in paths_by_arch}
    latest_version_info = {}

    for arch, paths in sorted_paths_by_arch.items():
        for lua_file_path, extracted_path in paths:
            parts = extracted_path.split('/')
            if len(parts) != 3:
                write_output(f"Unexpected path structure: {extracted_path}")
                continue

            category, package, version = parts
            category = category.capitalize()

            if (category, package) not in latest_version_info:
                latest_version_info[(category, package)] = {}

            if arch not in latest_version_info[(category, package)]:
                module_info, creation_date, installer = extract_lua_info(lua_file_path)
                if module_info is None:
                    continue

                latest_version_info[(category, package)][arch] = (module_info, creation_date, installer)

            if (category, package, version) not in package_infos[arch]:
                package_infos[arch][(category, package, version)] = (lua_file_path, version)

    package_infos_str_keys = {arch: {f"{cat}|{pkg}|{ver}": val for (cat, pkg, ver), val in infos.items()} for arch, infos in package_infos.items()}
    latest_version_info_str_keys = {f"{cat}|{pkg}": {arch: val for arch, val in infos.items()} for (cat, pkg), infos in latest_version_info.items()}
    collected_data = {
        'package_infos': package_infos_str_keys,
        'latest_version_info': latest_version_info_str_keys
    }

    save_collected_data(config.DATA_FILE, collected_data)


if __name__ == "__main__":
    
    write_log(config.log_file_path)
    write_log(config.broken_symlinks_file)

    collect_data()

    process_broken_symlinks()
