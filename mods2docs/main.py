import argparse
import importlib
from mods2docs import config, utils
import logging

def load_module(module_type, module_name):
    """
    Dynamically loads a module from the specified type (writer or parser) and name.
    """
    try:
        return importlib.import_module(f"mods2docs.{module_type}.{module_name}")
    except ImportError as e:
        logging.error(f"mods2docs.{module_type}.{module_name} module not found.")
        raise e

def main(writer_module, parser_module):
    logging.info("Starting main process")
    utils.write_log(config.main_log_file)
    writer_module.setup_writer_directories()

    for title, output_dir in zip(config.titles, config.output_dirs):
        logging.info(f"Processing {title} in directory {output_dir}")

        # Use the selected parser module to process data
        package_infos, latest_version_info, package_ref = parser_module.process_modulepath(config.modulepaths, title,
                                                                                           output_dir)

        # Use the selected writer module to write files
        writer_module.write_all_files(title, output_dir, package_infos, package_ref, latest_version_info)

    # Write global files that are needed only once
    writer_module.write_global_files(config)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Choose writer and parser modules")
    parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")
    parser.add_argument("--writer", required=True, help="Choose the writer module to use")
    parser.add_argument("--parser", required=True, help="Choose the parser module to use")
    args = parser.parse_args()

    # Set up logging based on verbosity
    utils.setup_logging(args.verbose)

    # Dynamically load writer and parser modules
    writer_module = load_module("writer", args.writer)
    parser_module = load_module("parser", args.parser)

    # Run main
    main(writer_module, parser_module)
