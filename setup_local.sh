#!/bin/bash
source ~/.bashrc
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

