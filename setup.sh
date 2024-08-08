#!/bin/bash
CONDA_MODULE="Anaconda3"
ENV_NAME="lmod_env"

echo "Purging modules and loading '$CONDA_MODULE' ..."
module purge && module load $CONDA_MODULE 

# Check if the Conda environment exists
if conda info --envs | grep -q "^$ENV_NAME\s"; then
  echo "Conda environment '$ENV_NAME' exists, activating ..."
  source activate $ENV_NAME
else
  echo "Creating Conda environment '$ENV_NAME'..."
  conda create -n lmod_env python=3.9 -y
  echo "Conda environment '$ENV_NAME' created, activating ..."
  source activate $ENV_NAME 
  echo "Installing required packages in '$ENV_NAME' ..."
  pip install lupa packaging # packaging currently unused
  echo "Conda environment '$ENV_NAME' created and packages installed."
fi
