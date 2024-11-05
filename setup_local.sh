#!/bin/bash
# This script sets up a Conda environment named 'lmod_env' for the required Python packages.
# It assumes Conda is initialized (via ~/.bashrc) and the environment does not already exist.
# If 'lmod_env' is missing, the script will create it with Python 3.9 and install necessary packages:
# - lupa: for embedding Lua in Python, often used in HPC modules
# - packaging: for parsing and comparing version numbers
# - hpc-rocket: for handling HPC job submissions
source ~/.bashrc  # Assumes Conda is initialised

ENV_NAME="lmod_env"

# Activate the Conda environment
echo "Activating Conda environment '$ENV_NAME' ..."
conda activate $ENV_NAME

# If the environment doesn't exist, create it and install the required packages
if [ $? -ne 0 ]; then
  echo "Conda environment '$ENV_NAME' not found. Creating it..."
  conda create -n $ENV_NAME python=3.9 -y
  wait
  conda activate $ENV_NAME
  wait
  echo "Installing required packages in '$ENV_NAME' ..."
  pip install lupa packaging hpc-rocket
fi

echo "Environment setup is complete."


