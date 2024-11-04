import os
import pickle
import logging
from mods2docs import config

def setup_logging(verbose, logfile=None):
    """
    Configures logging with different levels for console and file output.

    Args:
        verbose (bool): If True, sets console logging to DEBUG level; otherwise, INFO level.
        logfile (str, optional): Path to a file for logging output. If provided, all logs are saved here at DEBUG level.
    """
    # Define the logging format
    log_format = "%(asctime)s - %(levelname)s - %(message)s"

    # Set up root logger to handle all logs
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    # Console handler with level based on verbosity
    console_handler = logging.StreamHandler()
    console_level = logging.DEBUG if verbose else logging.INFO
    console_handler.setLevel(console_level)
    console_handler.setFormatter(logging.Formatter(log_format))

    # File handler at DEBUG level to capture all logs
    if logfile:
        file_handler = logging.FileHandler(logfile, mode='w')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(log_format))
        logging.getLogger().addHandler(file_handler)

    # Attach only the console handler to the root logger
    logging.getLogger().addHandler(console_handler)

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

def save_collected_data(file_path, data):
    """Saves collected data as a pickle file."""
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)

def load_module(module_type, module_name):
    """
    Dynamically loads a module from the specified type (writer or parser) and name.
    """
    try:
        return importlib.import_module(f"mods2docs.{module_type}.{module_name}")
    except ImportError as e:
        logging.error(f"mods2docs.{module_type}.{module_name} module not found.")
        raise e
