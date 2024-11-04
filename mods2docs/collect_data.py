import os
import pickle
import logging
import argparse
import importlib
from mods2docs import utils, config


def collect_data(parser_module):
    """Collects and organises Lua module data by architecture using the specified parser module."""
    paths_by_arch = parser_module.gather_lua_paths_by_arch()
    sorted_paths_by_arch = parser_module.sort_paths(paths_by_arch)

    package_infos = {arch: {} for arch in paths_by_arch}
    latest_version_info = {}

    # Process each architecture’s paths
    for arch, paths in sorted_paths_by_arch.items():
        parser_module.process_paths_for_architecture(paths, arch, parser_module, latest_version_info, package_infos)

    # Convert keys to strings for serialization
    package_infos_str_keys = {
        arch: {f"{cat}|{pkg}|{ver}": val for (cat, pkg, ver), val in infos.items()}
        for arch, infos in package_infos.items()
    }
    latest_version_info_str_keys = {
        f"{cat}|{pkg}": {arch: val for arch, val in infos.items()}
        for (cat, pkg), infos in latest_version_info.items()
    }

    collected_data = {
        'package_infos': package_infos_str_keys,
        'latest_version_info': latest_version_info_str_keys
    }

    utils.save_collected_data(config.DATA_FILE, collected_data)

def main(parser_module):
    utils.write_log(config.log_file_path)
    utils.write_log(config.broken_symlinks_file)

    collect_data(parser_module)
    parser_module.process_broken_symlinks()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run data collection with a specified parser module.")
    parser.add_argument("--parser", default="lmod", help="Choose the parser module to use")
    args = parser.parse_args()

    # Dynamically import the specified parser module
    parser_module = utils.load_module("parser", args.parser)

    # Run main with the specified parser module
    main(parser_module)
