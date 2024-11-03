import subprocess

def extract_installer(file_path):
    try:
        result = subprocess.run(['ls', '-lrath', file_path], capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                parts = line.split()
                if len(parts) > 2 and parts[2].startswith('sa_'):
                    return parts[2][3:]
    except Exception as e:
        append_log(f"Error extracting installer: {e}", config.log_file_path)
    return None

def save_collected_data(file_path, data):
    """Saves collected data as a pickle file."""
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)

