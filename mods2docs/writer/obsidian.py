import os
import re
from datetime import datetime
from mods2docs import config, utils
from mods2docs.writer.common import setup_writer_directories

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
    utils.append_file(package_file, content)

def write_all_files(title, output_dir, package_infos, package_ref, latest_version_info):

    output_dir = os.path.join(config.DATA_FOLDER, output_dir)
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

                module_info: object
                module_info, creation_date, installer = latest_version_info[key][arch]
                latest_creation_dates[arch] = creation_date
                dependencies.update(module_info.get('Loaded Modules', []))

        latest_info_arch = 'icelake' if latest_versions.get('icelake') else 'znver3'
        latest_info = latest_version_info.get(key, {}).get(latest_info_arch, (None, None, None))[0]

        if latest_info is None:
            utils.append_log(f"Warning: Missing latest info for {primary_category} | {package}. Skipping.",config.main_log_file)
            continue

        if package not in all_category_packages:
            write_package_file(package, output_dir, list(dependencies), moduleclass)
            all_category_packages.add(package)

def write_global_files(config):
    """
    Placeholder for writing global files in the obsidian writer.
    
    Currently, no global files are required for obsidian, but this function
    is available for future needs.
    
    Args:
        config (module or dict-like object): Contains configuration settings.
    """
    pass  # No action needed at this time
