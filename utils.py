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

def make_reference(*args):
    return '-'.join(args).replace(' ', '-').lower()
# Alias
make_filename = make_reference

def write_log(message):
    if message is None:
        message = ""
    with open(config.main_log_file, 'a') as f:
        f.write(message + '\n')
    if verbose:
        print(message)
