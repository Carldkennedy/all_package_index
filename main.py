import os
import re
import pickle
import subprocess
import datetime
import argparse
import config
from packaging import version
from utils import append_file, load_collected_data, make_reference, make_filename
from parser.lmod import run_collect_data_script

os.makedirs(config.IMPORTS_DIR, exist_ok=True)
os.makedirs(config.STACKS_DIR, exist_ok=True)
os.makedirs(config.CUSTOM_DIR, exist_ok=True)

def write_log():
    with open(config.main_log_file, 'w') as log_file:
        log_file.write("")

def write_output(message):
    if message is None:
        message = ""
    with open(config.main_log_file, 'a') as f:
        f.write(message + '\n')
    if verbose:
        print(message)

def write_file(filepath, content):
    with open(filepath, 'w') as file:
        file.write(content)




def write_package_file(category_dir, category, package, output_dir):
    package_file = os.path.join(category_dir, f"{package}.rst")
    content = (
        f".. _{make_reference(package, category, output_dir)}:\n\n"
        f"{package}\n{'=' * len(package)}\n\n"
        f".. include:: /{config.IMPORTS_DIR}/{make_filename(package, 'sdbr', output_dir)}.rst\n\n"
        f".. include:: /{config.IMPORTS_DIR}/{make_filename(package, 'dscr', output_dir)}.rst\n\n"
        f".. include:: /{config.IMPORTS_DIR}/packages_note.rst\n\n"
        f".. include:: /referenceinfo/imports/scheduler/SLURM/common_commands/srun_start_interactive_session_import_stanage.rst\n\n"
        f"A version of {package} can then be made available with *one* of the following:\n\n"
        f".. include:: /{config.IMPORTS_DIR}/{make_filename(package, 'ml', output_dir)}.rst\n\n"
        f".. include:: /{config.CUSTOM_DIR}/{make_filename(package, 'cust', output_dir)}.rst\n\n"
        f"Notes\n-----\n\n"
        f".. include:: /{config.IMPORTS_DIR}/{make_filename(package, 'inst', output_dir)}.rst\n\n"
        f".. include:: /{config.IMPORTS_DIR}/{make_filename(package, 'dpnd', output_dir)}.rst\n\n"
    )
    write_file(package_file, content)

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
        if icelake_info:
            version_number_icelake = icelake_info[0].get('EB Version', None)
            if version_number_icelake is None:
                # Fallback: Extract version from the directory name if EB Version is not available
                version_number_icelake = extract_version(icelake_info[0].get('Root', 'N/A').split('/')[-1])
            creation_date_icelake = icelake_info[1]
            # Extract URL from WhatIs Information
            homepage_url = next((info.split(': ')[1] for info in icelake_info[0].get('WhatIs Information', []) if info.startswith('URL:')), 'N/A')

        # Get information for Znver3 architecture
        znver_info = latest_version_info[key].get('znver3', None)
        if znver_info:
            version_number_znver = znver_info[0].get('EB Version', None)
            if version_number_znver is None:
                # Fallback: Extract version from the directory name if EB Version is not available
                version_number_znver = extract_version(znver_info[0].get('Root', 'N/A').split('/')[-1])
            creation_date_znver = znver_info[1]
            # Update URL if available in Znver3 info
            if homepage_url == 'N/A':
                homepage_url = next((info.split(': ')[1] for info in znver_info[0].get('WhatIs Information', []) if info.startswith('URL:')), 'N/A')

    # Write sidebar file content
    sdbr_file = os.path.join(config.IMPORTS_DIR, f"{make_filename(package, 'sdbr', output_dir)}.rst")
    content = (
        f".. sidebar:: {package}\n\n"
        f"   :Latest Version (Icelake): {version_number_icelake}\n"
        f"   :Installed on (Icelake): {creation_date_icelake}\n"
        f"   :Latest Version (Znver): {version_number_znver}\n"
        f"   :Installed on (Znver): {creation_date_znver}\n"
        f"   :URL: {homepage_url}\n"
    )
    write_file(sdbr_file, content)


def write_description_file(package, latest_info, output_dir):
    description = next((info for info in latest_info.get('WhatIs Information', []) if 'Description:' in info), 'No description available')
    dscr_file = os.path.join(config.IMPORTS_DIR, f"{make_filename(package, 'dscr', output_dir)}.rst")
    description = description.replace('*', '')
    description = "\n".join(line.strip() for line in description.split("\n")).strip() + '\n'
    description = description.replace('`time\'', '``time``')
    description = re.sub(r'Description:\s*', '', description)
    write_file(dscr_file, f"{description}\n")

def write_installation_file(package, latest_info, output_dir):
    inst_file = os.path.join(config.IMPORTS_DIR, f"{make_filename(package, 'inst', output_dir)}.rst")
    ebroot_var= latest_info.get('EB Variables', {}).get('EBROOT', {}).get('var_name', None)
    if ebroot_var is None:
        content = (
            f"The latest version of {package} was installed manually."
        )
    else:
        content = (
            f"{package} was installed using Easybuild, build details can be found in ``${ebroot_var}/easybuild`` with a given module loaded."
        )
    append_file(inst_file, content + "\n")

def write_custom_file(package, output_dir):
    cust_file = os.path.join(config.CUSTOM_DIR, f"{make_filename(package, 'cust', output_dir)}.rst")
    write_file(cust_file, "")

def write_dependencies(dependencies, output_dir, category, package, package_ref):
    dpnd_file = os.path.join(config.IMPORTS_DIR, f"{make_filename(package, 'dpnd', output_dir)}.rst")
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
            dep_link = f":ref:`{dep} <{make_reference(dep_package, ref_category, output_dir)}>`"
            content += f"   - {dep_link}\n"
    else:
        content = ""
    write_file(dpnd_file, content)

def write_ml_file(package, package_infos, output_dir):
    import_file = os.path.join(config.IMPORTS_DIR, f"{make_filename(package, 'ml', output_dir)}.rst")

    # Initialize the file with .. tabs:: only if it's newly created
    if not os.path.exists(import_file):
        write_file(import_file, ".. tabs::\n\n")

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




def process_modulepath(modulepaths, title, output_dir):
    # Run collect_data.py if data file doesn't exist
    if not os.path.exists(config.DATA_FILE):
        print("Collected data not found. Running collect_data.py...")
        write_output("Collected data not found. Running collect_data.py...")
        run_collect_data_script()

    collected_data = load_collected_data(config.DATA_FILE)
    if not collected_data:
        print("No collected data found even after running collect_data.py.")
        write_output("No collected data found even after running collect_data.py.")
        return

    package_infos = collected_data.get('package_infos', {})
    latest_version_info = collected_data.get('latest_version_info', {})

    # Initialize a dictionary to hold the primary category for each package
    package_ref = {}
    
    # Iterate over each key in the latest_version_info dictionary
    for key in latest_version_info.keys():
        categories = set()  # Initialize a new set for categories for each key
        
        # Extract category and package for each architecture entry
        for arch in latest_version_info[key]:
            category, package = key.split('|')
            categories.add(category)  # Add category to the set
    
        # Check if the package already has a category assigned
#        if package not in package_ref:
#            # Assign the first non-"All" category or "All" if none exists
#            primary_category = next((cat for cat in categories if cat != "All"), "All")
#            package_ref[package] = primary_category
#        elif "All" in categories and package_ref[package] == "All":
#            # Overwrite with "All" only if it's the only category available
#            package_ref[package] = "All"

        if package not in package_ref:
            # Assign the first non-"All" category or "All" if none exists
            primary_category = next((cat for cat in categories if cat != "All"), "All")
            package_ref[package] = primary_category
        else:
            # Optional: Update logic to potentially overwrite "All" with other categories
            if package_ref[package] == "All":
                non_all_category = next((cat for cat in categories if cat != "All"), None)
                if non_all_category:
                    package_ref[package] = non_all_category
 
    # Create stacks index file
    output_dir_path = os.path.join(config.STACKS_DIR, output_dir)
    os.makedirs(output_dir_path, exist_ok=True)
    stack_index_file = os.path.join(output_dir_path, "index.rst")
    title_underline = "=" * len(title)
    write_file(stack_index_file, f".. _{make_reference(output_dir, '', '')}:\n\n{title}\n{title_underline}\n\n.. toctree::\n    :maxdepth: 1\n    :glob:\n\n")

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
        write_file(all_category_index_file, f".. _{make_reference(output_dir, all_category, '')}:\n\n{all_category_title}\n{'^' * len(all_category_title)}\n\nModule class description: {module_class}\n\n.. toctree::\n    :maxdepth: 1\n    :glob:\n\n    ./*\n\n")
        append_file(stack_index_file, f"    {all_category}/index.rst\n\n")
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
                write_file(category_index_file, f".. _{make_reference(output_dir, primary_category, '')}:\n\n{category_title}\n{'^' * len(category_title)}\n\nModule class description: {module_class}\n\n.. toctree::\n    :maxdepth: 1\n    :glob:\n\n    ./*\n\n")
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
            write_output(f"Warning: Missing latest info for {primary_category} | {package}. Skipping.")
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

        link = f"* :ref:`{package} <{make_reference(package, primary_category, output_dir)}>`\n"
        links_for_all_index.append(link) 

    # Write sorted lines to the file
    links_for_all_index.sort(key=str.casefold)
    with open(all_category_index_file, 'a') as file:
        file.writelines(links_for_all_index)

    links_for_main_index.sort(key=str.casefold)
    with open(stack_index_file, 'a') as file:
        file.writelines(links_for_main_index)
def main():

    write_log()

    for title, output_dir in zip(config.titles, config.output_dirs):
        print(f"Processing {title} in directory {output_dir}")
        process_modulepath(config.modulepaths, title, output_dir)

    stacks_title = "All Packages Index"
    stacks_file = os.path.join(config.STACKS_DIR, "index.rst")
    write_file(stacks_file, f"{stacks_title}\n{'=' * len(stacks_title)}\n\nLast updated: {config.current_date}\n\n.. toctree::\n    :maxdepth: 1\n    :glob:\n\n")

    for output_dir in config.output_dirs:
        append_file(stacks_file, f"    {output_dir}/index\n")

    note_file = os.path.join(config.IMPORTS_DIR, "packages_note.rst")
    write_file(note_file, f".. note::\n\n   This is an autogenerated page, more detail including examples may be available for this package. Please see :ref:`stanage-software`\n")

if __name__ == "__main__":
    global verbose
    verbose = False
    parser = argparse.ArgumentParser(description="Increases verbosity of logs to screen if -v is passed")
    parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")
    args = parser.parse_args()

    if args.verbose:
        verbose = True

    main()
