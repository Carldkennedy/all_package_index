#!/bin/bash

# This script sets up a Conda environment named '$ENV_NAME' for the required Python packages.
# Assumes Conda is initialized (via ~/.bashrc) and the environment does not already exist.
# If '$ENV_NAME' is missing, the script will create it with Python 3.9 and install necessary packages:
# - lupa: for embedding Lua in Python, often used in HPC modules
# - packaging: for parsing and comparing version numbers
# - hpc-rocket: for handling HPC job submissions

# Dynamically detect the base directory of Conda
CONDA_BASE=$(conda info --base 2>/dev/null)

if [ -z "$CONDA_BASE" ]; then
	    echo "Error: Conda is not installed or not in the PATH."
	    exit 1
fi

# Source Conda's environment script
if [ -f "$CONDA_BASE/etc/profile.d/conda.sh" ]; then
	    source "$CONDA_BASE/etc/profile.d/conda.sh"
    else
	    echo "Error: Conda initialization script not found at $CONDA_BASE/etc/profile.d/conda.sh."
	    exit 1
fi


# source ~/.bashrc  # Assumes Conda is initialised
source config.env

# Activate the Conda environment
echo "Activating Conda environment '$ENV_NAME' ..."
conda activate $ENV_NAME

# Check if the activation succeeded
if [ $? -ne 0 ]; then
    echo "Conda environment '$ENV_NAME' not found. Creating it..."
    conda create -n $ENV_NAME python=3.9 -y
    if [ $? -ne 0 ]; then
        echo "Error creating Conda environment. Exiting."
        exit 1
    fi
    wait
    conda activate $ENV_NAME
    if [ $? -ne 0 ]; then
        echo "Error activating Conda environment after creation. Exiting."
        exit 1
    fi
    echo "Installing required packages in '$ENV_NAME' ..."
    eval "$INSTALL_REQUIRED_PACKAGES"
    if [ $? -ne 0 ]; then
        echo "Error installing required packages. Exiting."
        exit 1
    fi
fi

echo "Environment setup is complete."

