import os
import re
import pickle
import subprocess
import datetime
import argparse
import pprint
import config
from utils import append_file

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


def make_reference(*args):
    return '-'.join(args).replace(' ', '-').lower()

def make_filename(*args):
    return '-'.join(args).replace(' ', '-').lower()
####################################################
def write_package_file(package, output_dir, dependencies, moduleclass):
    os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists
    package_file = os.path.join(output_dir, f"{package}.md")
    content = f"#{moduleclass}\n"
    if dependencies:
        sorted_dependencies = sorted(dependencies)
        sorted_dependencies_package_only = [s.split('/')[0] for s in sorted_dependencies]
        unique_sorted_dependencies_package_only = list(set(sorted_dependencies_package_only)) 
        for dep in unique_sorted_dependencies_package_only:
            content += f"[[{dep}]]\n"
    print(f"Writing to {package_file}")
    append_file(package_file, content)
####################################################

def load_collected_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    return None

def run_collect_data_script():
    try:
        result = subprocess.run(['python', 'collect_data.py'], check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        write_output(f"Failed to run collect_data.py: {e}")
        print(f"Failed to run collect_data.py: {e}")
        return False

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
        if package not in package_ref:
            # Assign the first non-"All" category or "All" if none exists
            primary_category = next((cat for cat in categories if cat != "All"), "All")
            package_ref[package] = primary_category
        elif "All" in categories and package_ref[package] == "All":
            # Overwrite with "All" only if it's the only category available
            package_ref[package] = "All"
    current_category = "" 
    added_indexes = set()
    all_category_packages = set()
    for package, primary_category in package_ref.items():

        if primary_category != current_category:
            current_category = primary_category
            moduleclass = primary_category.lower()
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
            write_package_file(package, output_dir, list(dependencies), moduleclass)
            all_category_packages.add(package)

def main():

    write_log()

    for title, output_dir in zip(config.titles, config.output_dirs):
        print(f"Processing {title} in directory {output_dir}")
        process_modulepath(config.modulepaths, title, output_dir)

if __name__ == "__main__":
    global verbose
    verbose = False
    parser = argparse.ArgumentParser(description="Increases verbosity of logs to screen if -v is passed")
    parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")
    args = parser.parse_args()

    if args.verbose:
        verbose = True

    main()
