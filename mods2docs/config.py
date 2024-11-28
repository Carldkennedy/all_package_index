import os
import json
import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv("config.env")

# General settings
current_date = datetime.datetime.now().strftime(os.getenv("CURRENT_DATE_FORMAT"))

# Paths
DATA_DIR = Path(os.getenv("DATA_DIR"))
STACKS_DIR = DATA_DIR / os.getenv("STACKS_DIR")
IMPORTS_DIR = DATA_DIR / os.getenv("IMPORTS_DIR")
CUSTOM_DIR = DATA_DIR / os.getenv("CUSTOM_DIR")

# File paths
broken_symlinks_file = DATA_DIR / os.getenv("BROKEN_SYMLINKS_FILE")
log_file_path = DATA_DIR / os.getenv("LOG_FILE")
main_log_file = DATA_DIR / os.getenv("MAIN_LOG_FILE")
DATA_FILE = DATA_DIR / os.getenv("DATA_FILE")

# SLURM interactive session file
SLURM_INTERACTIVE_SESSION_IMPORT = os.getenv("SLURM_INTERACTIVE_SESSION_IMPORT")

# Module paths (parsed from JSON string)
modulepaths = json.loads(os.getenv("MODULEPATHS"))

# Titles and output directories (parsed from JSON strings)
titles = json.loads(os.getenv("TITLES"))
output_dirs = json.loads(os.getenv("OUTPUT_DIRS"))

# Module classes (parsed from JSON string)
module_classes = json.loads(os.getenv("MODULE_CLASSES"))
