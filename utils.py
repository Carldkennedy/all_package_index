

def append_file(filepath, content):  
    with open(filepath, 'a') as file:
        file.write(content)

def load_collected_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    return None
