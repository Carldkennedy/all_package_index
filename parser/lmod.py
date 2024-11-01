import subprocess
import os
import config
from utils import append_file, append_log

def run_collect_data_script():
    try:
        result = subprocess.run(['python', 'collect_data.py'], check=True) 
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        append_log(f"Failed to run collect_data.py: {e}", config.main_log_file)
        print(f"Failed to run collect_data.py: {e}")
        return False

def process_broken_symlinks():
    if not os.path.exists(config.broken_symlinks_file):
        print(f"No broken symlinks file found for date: {config.current_date}")
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

def extract_package_info(collected_data):
    """
    Extracts package information, latest version info, and categorizes each package
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

