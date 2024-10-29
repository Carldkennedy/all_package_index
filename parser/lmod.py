def run_collect_data_script():
    try:
        result = subprocess.run(['python', 'collect_data.py'], check=True) 
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        write_output(f"Failed to run collect_data.py: {e}")
        print(f"Failed to run collect_data.py: {e}")
        return False
