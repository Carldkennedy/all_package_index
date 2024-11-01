import os
import argparse
import config
from utils import load_collected_data, make_reference, write_file, append_file, write_log, append_log
from parser.lmod import run_collect_data_script
from writer.rest import write_custom_file, write_dependencies, write_description_file, write_installation_file, \
    write_ml_file, write_package_file, write_sidebar_file, write_all_files

os.makedirs(config.IMPORTS_DIR, exist_ok=True)
os.makedirs(config.STACKS_DIR, exist_ok=True)
os.makedirs(config.CUSTOM_DIR, exist_ok=True)

def process_modulepath(modulepaths, title, output_dir):
    # Run collect_data.py if data file doesn't exist
    if not os.path.exists(config.DATA_FILE):
        print("Collected data not found. Running collect_data.py...")
        append_log("Collected data not found. Running collect_data.py...", config.main_log_file)
        run_collect_data_script()

    collected_data = load_collected_data(config.DATA_FILE)
    if not collected_data:
        print("No collected data found even after running collect_data.py.")
        append_log("No collected data found even after running collect_data.py.", config.main_log_file)
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


write_all_files(title, package_infos, output_dir, package_ref, latest_version_info)

def main():

    write_log(config.main_log_file)

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
