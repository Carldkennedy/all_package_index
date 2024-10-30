import subprocess
import os
import config
def run_collect_data_script():
    try:
        result = subprocess.run(['python', 'collect_data.py'], check=True) 
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        write_log(f"Failed to run collect_data.py: {e}")
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
