import argparse
import config
import utils
from parser import lmod
from writer import rest

def main():

    utils.write_log(config.main_log_file)

    rest.setup_writer_directories()

    for title, output_dir in zip(config.titles, config.output_dirs):
        print(f"Processing {title} in directory {output_dir}")
        package_infos, latest_version_info, package_ref = lmod.process_modulepath(config.modulepaths, title, output_dir)
        rest.write_all_files(title, output_dir, package_infos, package_ref, latest_version_info)

    rest.write_stacks_index(config.STACKS_DIR, config.current_date, config.output_dirs)

    rest.write_note_file(config.IMPORTS_DIR)

if __name__ == "__main__":
    global verbose
    verbose = False
    parser = argparse.ArgumentParser(description="Increases verbosity of logs to screen if -v is passed")
    parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")
    args = parser.parse_args()

    if args.verbose:
        verbose = True

    main()
