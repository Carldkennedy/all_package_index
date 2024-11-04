#Common writer functions
import os
from mods2docs import config

def setup_writer_directories():
    os.makedirs(config.IMPORTS_DIR, exist_ok=True)
    os.makedirs(config.STACKS_DIR, exist_ok=True)
    os.makedirs(config.CUSTOM_DIR, exist_ok=True)
