

def append_file(filepath, content):  
    with open(filepath, 'a') as file:
        file.write(content)
