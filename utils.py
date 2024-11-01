import os
import pickle
import config

def make_filename(*args):
    return '-'.join(args).replace(' ', '-').lower()
# Alias - to ease reading code
make_reference = make_filename

def write_file(filepath, content):
    with open(filepath, 'w') as file:
        file.write(content)

def append_file(filepath, content):  
    with open(filepath, 'a') as file:
        file.write(content)

def write_log(logfile):
    with open(logfile, 'w') as log_file:
        log_file.write("")

def append_log(message, logfile):
    if message is None:
        message = ""
    with open(logfile, 'a') as f:
        f.write(message + '\n')

def load_collected_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    return None

def ensure_data_collected():
    """
    Ensures that the collected data is available by checking if the data file exists.
    If not, it runs the data collection script and loads the data.

    Returns:
        dict or None: The collected data if available; otherwise, None.
    """
    if not os.path.exists(config.DATA_FILE):
        print("Collected data not found. Running collect_data.py...")
        utils.append_log("Collected data not found. Running collect_data.py...", config.main_log_file)
        lmod.run_collect_data_script()

    collected_data = load_collected_data(config.DATA_FILE)
    if not collected_data:
        print("No collected data found even after running collect_data.py.")
        utils.append_log("No collected data found even after running collect_data.py.", config.main_log_file)
        return None

    return collected_data

