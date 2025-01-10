import os
import re
from datetime import datetime
from mods2docs import config, utils
from mods2docs.writer.common import setup_writer_directories
# Functions to write rst files


def write_stacks_index(stacks_dir, current_date, output_dirs):
    """
    Writes the main stacks index file with a title, date, table of contents,
    and appends each output directory to the index file.

    Args:
        stacks_dir (str): The directory where the stacks index file will be created.
        current_date (str): The date to include in the index file.
        output_dirs (list): List of directories to add to the index file.
    """
    # Define the initial content with title and date
    stacks_title = "All Packages Index"
    stacks_file = os.path.join(stacks_dir, "index.rst")
    initial_content = (
        f"{stacks_title}\n{'=' * len(stacks_title)}\n\n"
        f"Last updated: {current_date}\n\n"
        ".. toctree::\n"
        "    :maxdepth: 1\n"
        "    :glob:\n\n"
    )

    utils.write_file(stacks_file, initial_content)

    for output_dir in output_dirs:
        utils.append_file(stacks_file, f"    {output_dir}/index\n")

def write_note_file(imports_dir):
    """
    Writes a note file in the imports directory to be imported into all packages.

    Args:
        imports_dir (str): The directory where the note file will be created.
    """
    note_file = os.path.join(imports_dir, "packages_note.rst")
    content = (
        ".. note::\n\n"
        "   This is an autogenerated page, more detail including examples may be available for this package. "
        "Please see the first section of :ref:`stanage-software`\n"
    )

    utils.write_file(note_file, content)

def write_package_file(category_dir, category, package, output_dir):
    package_file = os.path.join(category_dir, f"{package}.rst")
    content = (
        f".. _{utils.make_reference(package, category, output_dir)}:\n\n"
        f"{package}\n{'=' * len(package)}\n\n"
        f".. include:: /{config.IMPORTS_DIR}/{utils.make_filename(package, 'sdbr', output_dir)}.rst\n\n"
        f".. include:: /{config.IMPORTS_DIR}/{utils.make_filename(package, 'dscr', output_dir)}.rst\n\n"
        f".. include:: /{config.IMPORTS_DIR}/packages_note.rst\n\n"
        f".. include:: /{config.SLURM_INTERACTIVE_SESSION_IMPORT}\n\n"
        f"A version of {package} can then be made available with *one* of the following:\n\n"
        f".. include:: /{config.IMPORTS_DIR}/{utils.make_filename(package, 'ml', output_dir)}.rst\n\n"
        f".. include:: /{config.CUSTOM_DIR}/{utils.make_filename(package, 'cust', output_dir)}.rst\n\n"
        f"Notes\n-----\n\n"
        f".. include:: /{config.IMPORTS_DIR}/{utils.make_filename(package, 'inst', output_dir)}.rst\n\n"
        f".. include:: /{config.IMPORTS_DIR}/{utils.make_filename(package, 'dpnd', output_dir)}.rst\n\n"
    )
    utils.write_file(package_file, content)

def write_sidebar_file(package, category, latest_version_info, output_dir):
    def extract_version(version_with_toolchain):
        """Extracts the version number from a version string, removing toolchain if present."""
        match = re.match(r'^[^-]+(?:-[^-0-9][^-]*)', version_with_toolchain)
        if match:
            return match.group(0)
        return version_with_toolchain

    key = f"{category}|{package}"
    
    # Initialize version, date, and URL variables
    version_number_icelake = 'N/A'
    creation_date_icelake = 'N/A'
    version_number_znver = 'N/A'
    creation_date_znver = 'N/A'
    homepage_url = 'N/A'

    # Access the entry for the specific package and category
    if key in latest_version_info:
        # Get information for Icelake architecture
        icelake_info = latest_version_info[key].get('icelake', None)
        if icelake_info and len(icelake_info) > 0 and icelake_info[0]:
            version_number_icelake = icelake_info[0].get('EB Version', None)
            if version_number_icelake is None:
                # Fallback: Extract version from the directory name if EB Version is not available
                root = icelake_info[0].get('Root', 'N/A')
                version_number_icelake = extract_version(root.split('/')[-1] if root else 'N/A')
            creation_date_icelake = icelake_info[1] if len(icelake_info) > 1 else 'N/A'
            # Extract URL from WhatIs Information
            whatis_info = icelake_info[0].get('WhatIs Information', [])
            homepage_url = next((info.split(': ')[1] for info in whatis_info if info.startswith('URL:')), 'N/A')
    
        # Get information for Znver3 architecture
        znver_info = latest_version_info[key].get('znver3', None)
        if znver_info and len(znver_info) > 0 and znver_info[0]:
            version_number_znver = znver_info[0].get('EB Version', None)
            if version_number_znver is None:
                # Fallback: Extract version from the directory name if EB Version is not available
                root = znver_info[0].get('Root', 'N/A')
                version_number_znver = extract_version(root.split('/')[-1] if root else 'N/A')
            creation_date_znver = znver_info[1] if len(znver_info) > 1 else 'N/A'
            # Update URL if available in Znver3 info
            if homepage_url == 'N/A':
                whatis_info = znver_info[0].get('WhatIs Information', [])
                homepage_url = next((info.split(': ')[1] for info in whatis_info if info.startswith('URL:')), 'N/A')


    # Write sidebar file content
    sdbr_file = os.path.join(config.IMPORTS_DIR, f"{utils.make_filename(package, 'sdbr', output_dir)}.rst")
    content = (
        f".. sidebar:: {package}\n\n"
        f"   :Latest Version (Icelake): {version_number_icelake}\n"
        f"   :Installed on (Icelake): {creation_date_icelake}\n"
        f"   :Latest Version (Znver3): {version_number_znver}\n"
        f"   :Installed on (Znver3): {creation_date_znver}\n"
        f"   :URL: {homepage_url}\n"
    )
    utils.write_file(sdbr_file, content)

def write_description_file(package, latest_info, output_dir):
    description = next((info for info in latest_info.get('WhatIs Information', []) if 'Description:' in info), 'No description available')
    dscr_file = os.path.join(config.IMPORTS_DIR, f"{utils.make_filename(package, 'dscr', output_dir)}.rst")
    description = description.replace('*', '')
    description = "\n".join(line.strip() for line in description.split("\n")).strip() + '\n'
    description = description.replace('`time\'', '``time``')
    description = re.sub(r'Description:\s*', '', description)
    utils.write_file(dscr_file, f"{description}\n")

def write_installation_file(package, latest_info, output_dir):
    inst_file = os.path.join(config.IMPORTS_DIR, f"{utils.make_filename(package, 'inst', output_dir)}.rst")
    ebroot_var= latest_info.get('EB Variables', {}).get('EBROOT', {}).get('var_name', None)
    if ebroot_var is None:
        content = (
            f"The latest version of {package} was installed manually."
        )
    else:
        content = (
            f"{package} was installed using Easybuild, build details can be found in ``${ebroot_var}/easybuild`` with a given module loaded."
        )
    utils.write_file(inst_file, content + "\n")

def write_custom_file(package, output_dir):
    cust_file = os.path.join(config.CUSTOM_DIR, f"{utils.make_filename(package, 'cust', output_dir)}.rst")
    utils.write_file(cust_file, "")

def write_dependencies(dependencies, output_dir, category, package, package_ref):
    dpnd_file = os.path.join(config.IMPORTS_DIR, f"{utils.make_filename(package, 'dpnd', output_dir)}.rst")
    if dependencies:
        content = f".. dropdown:: Dependencies for latest version of {package}\n\n"
        def version_key(version):
            return [int(x) if x.isdigit() else x for x in re.split(r'(\d+)', version)]
        
        # Dictionary to store the latest version for each package
        latest_versions = {}
        
        # Iterate over the paths
        for dependency in dependencies:
            package, version = dependency.split('/')[:2]
            # Store the latest version using dict, which will naturally keep the last inserted version
            if package not in latest_versions or version_key(version) > version_key(latest_versions[package]):
                latest_versions[package] = version
        
        # Collect the latest package versions
        latest_package_versions = [f"{pkg}/{ver}" for pkg, ver in latest_versions.items()]
        sorted_dependencies = sorted(latest_package_versions, key=str.casefold) # case-insensitive sort

        for dep in sorted_dependencies:
            dep_package = dep.split('/')[0]
            ref_category = package_ref.get(dep_package, 'unknown')
            dep_link = f":ref:`{dep} <{utils.make_reference(dep_package, ref_category, output_dir)}>`"
            content += f"   - {dep_link}\n"
    else:
        content = ""
    utils.write_file(dpnd_file, content)

def write_ml_file(package, package_infos, output_dir):
    import_file = os.path.join(config.IMPORTS_DIR, f"{utils.make_filename(package, 'ml', output_dir)}.rst")

    # Initialize the file with .. tabs:: only if it's newly created
    if not os.path.exists(import_file):
        utils.write_file(import_file, ".. tabs::\n\n")

    with open(import_file, 'r') as imp_f:
        existing_content = imp_f.read()

    # Initialize entries for architectures
    entries = {'icelake': [], 'znver3': []}

    # Collect module load lines for each architecture
    for arch in package_infos:
        versions = [key.split('|')[2] for key in package_infos[arch] if key.split('|')[1] == package]
        entries[arch].extend([f"            module load {package}/{ver}\n" for ver in versions])

    # Remove duplicates
    for arch in entries:
        entries[arch] = list(dict.fromkeys(entries[arch]))

    # Prepare content to be added
    content_dict = {'icelake': '', 'znver3': ''}

    # Add content for icelake if it doesn't already exist
    if entries['icelake'] and "    .. group-tab:: Icelake" not in existing_content:
        content_dict['icelake'] = "    .. group-tab:: Icelake\n\n        .. code-block:: console\n\n" + ''.join(entries['icelake']) + "\n"
    elif entries['icelake']:
        new_icelake_content = re.sub(
            r"(    .. group-tab:: Icelake\n\n        .. code-block:: console\n\n)((?:\n|.)*?)(\n\s*.. group-tab::|\Z)",
            lambda match: match.group(1) + ''.join(entries['icelake']) + match.group(3),
            existing_content,
            flags=re.MULTILINE
        )
        content_dict['icelake'] = new_icelake_content

    # Add content for znver3 if it doesn't already exist
    if entries['znver3'] and "    .. group-tab:: Znver3" not in existing_content:
        content_dict['znver3'] = "\n    .. group-tab:: Znver3\n\n        .. code-block:: console\n\n" + ''.join(entries['znver3']) + "\n"
    elif entries['znver3']:
        new_znver3_content = re.sub(
            r"(    .. group-tab:: Znver3\n\n        .. code-block:: console\n\n)((?:\n|.)*?)(\n\s*.. group-tab::|\Z)",
            lambda match: match.group(1) + ''.join(entries['znver3']) + match.group(3),
            existing_content,
            flags=re.MULTILINE
        )
        content_dict['znver3'] = new_znver3_content

    # Reconstruct the new content for the file
    new_content = existing_content

    # Ensure .. tabs:: is at the start
    if not new_content.startswith(".. tabs::"):
        new_content = ".. tabs::\n\n" + new_content

    if content_dict['icelake'] and "    .. group-tab:: Icelake" not in new_content:
        new_content += content_dict['icelake']
    if content_dict['znver3'] and "    .. group-tab:: Znver3" not in new_content:
        new_content += content_dict['znver3']

    # Write the final content back to the file
    with open(import_file, 'w') as imp_f:
        imp_f.write(new_content)

def write_all_files(title, output_dir, package_infos, package_ref, latest_version_info):
    # Create stacks index file
    output_dir_path = os.path.join(config.STACKS_DIR, output_dir)
    os.makedirs(output_dir_path, exist_ok=True)
    stack_index_file = os.path.join(output_dir_path, "index.rst")
    title_underline = "=" * len(title)
    utils.write_file(stack_index_file, f".. _{utils.make_reference(output_dir, '', '')}:\n\n{title}\n{title_underline}\n\n.. toctree::\n    :maxdepth: 1\n    :glob:\n\n")

    # Create All index file
    output_dir_path = os.path.join(config.STACKS_DIR, output_dir)
    current_category = ""
    added_indexes = set()
    all_category_packages = set()
    all_category = "All"
    all_category_dir = os.path.join(output_dir_path, all_category)
    os.makedirs(all_category_dir, exist_ok=True)
    all_category_index_file = os.path.join(all_category_dir, "index.rst")
    module_class = "All module classes"
    all_category_title = f"{all_category}"

    if all_category_index_file not in added_indexes:
        utils.write_file(all_category_index_file, f".. _{utils.make_reference(output_dir, all_category, '')}:\n\n{all_category_title}\n{'^' * len(all_category_title)}\n\n**{module_class}**\n\n.. toctree::\n    :maxdepth: 1\n    :glob:\n\n    ./*\n\n")
        utils.append_file(stack_index_file, f"    {all_category}/index.rst\n\n")
        added_indexes.add(all_category_index_file)

    links_for_all_index = []
    links_for_main_index = []
    for package, primary_category in package_ref.items():
        if primary_category != current_category:
            current_category = primary_category
            # Create other category indexes
            category_dir = os.path.join(output_dir_path, primary_category)
            os.makedirs(category_dir, exist_ok=True)
            category_index_file = os.path.join(category_dir, "index.rst")
            module_class = config.module_classes.get(primary_category.lower(), "")
            category_title = f"{primary_category}"
            if category_index_file not in added_indexes:
                utils.write_file(category_index_file, f".. _{utils.make_reference(output_dir, primary_category, '')}:\n\n{category_title}\n{'^' * len(category_title)}\n\n**{module_class}**\n\n.. toctree::\n    :maxdepth: 1\n    :glob:\n\n    ./*\n\n")
                #                append_file(stack_index_file, f"    {primary_category}/index.rst\n")
                link_main_index = f"    {primary_category}/index.rst\n"
                links_for_main_index.append(link_main_index)
                added_indexes.add(category_index_file)

        latest_versions = {}
        latest_creation_dates = {}
        dependencies = set()

        for arch in package_infos:
            key = f"{primary_category}|{package}"
            if key in latest_version_info and arch in latest_version_info[key]:
                latest_version = latest_version_info[key][arch][1]
                latest_versions[arch] = latest_version

                module_info, creation_date, installer = latest_version_info[key][arch]
                latest_creation_dates[arch] = creation_date
                dependencies.update(module_info.get('Loaded Modules', []))

        latest_info_arch = 'icelake' if latest_versions.get('icelake') else 'znver3'
        latest_info = latest_version_info.get(key, {}).get(latest_info_arch, (None, None, None))[0]

        if latest_info is None:
            append_log(f"Warning: Missing latest info for {primary_category} | {package}. Skipping.",
                       config.main_log_file)
            continue

        if package not in all_category_packages:
            write_package_file(category_dir, primary_category, package, output_dir)
            write_ml_file(package, package_infos, output_dir)
            write_description_file(package, latest_info, output_dir)
            write_sidebar_file(package, primary_category, latest_version_info, output_dir)
            write_installation_file(package, latest_info, output_dir)
            write_custom_file(package, output_dir)
            write_dependencies(list(dependencies), output_dir, primary_category, package, package_ref)

            all_category_packages.add(package)

        link = f"* :ref:`{package} <{utils.make_reference(package, primary_category, output_dir)}>`\n"
        links_for_all_index.append(link)

    # Write sorted lines to the file
    links_for_all_index.sort(key=str.casefold)
    with open(all_category_index_file, 'a') as file:
        file.writelines(links_for_all_index)

    links_for_main_index.sort(key=str.casefold)
    with open(stack_index_file, 'a') as file:
        file.writelines(links_for_main_index)

def write_global_files(config):
    """
    Writes global files that are needed only once, such as the stack index and note files.

    Args:
        config (module or dict-like object): Contains configuration settings, such as directories and dates.
    """
    stacks_dir = config.STACKS_DIR
    imports_dir = config.IMPORTS_DIR
    current_date = config.current_date
    output_dirs = config.output_dirs

    # Write stack index if the necessary fields are available
    if stacks_dir and current_date and output_dirs:
        write_stacks_index(stacks_dir, current_date, output_dirs)

    # Write note file if imports directory is available
    if imports_dir:
        write_note_file(imports_dir)
