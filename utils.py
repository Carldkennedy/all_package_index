import os
import config
import pickle

def write_file(filepath, content):
    with open(filepath, 'w') as file:
        file.write(content)

def append_file(filepath, content):  
    with open(filepath, 'a') as file:
        file.write(content)

def load_collected_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    return None

def make_filename(*args):
    return '-'.join(args).replace(' ', '-').lower()
# Alias
make_reference = make_filename

def write_log(logfile):
    with open(logfile, 'w') as log_file:
        log_file.write("")

def append_log(message, logfile):
    if message is None:
        message = ""
    with open(logfile, 'a') as f:
        f.write(message + '\n')
