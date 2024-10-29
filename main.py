import os
import re
import pickle
import subprocess
import datetime
import argparse
import config
from packaging import version
from utils import append_file, load_collected_data, make_reference, make_filename, write_file
from parser.lmod import run_collect_data_script
from writer.rest import write_custom_file, write_dependencies, write_description_file, write_installation_file, write_ml_file, write_package_file, write_sidebar_file

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
