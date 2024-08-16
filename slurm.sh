#!/bin/bash
#SBATCH --time=00:15:00
#SBATCH --mem=1G
#SBATCH --job-name=API-collect-data
#SBATCH --output=slurm.out

CONDA_MODULE="Anaconda3"
ENV_NAME="lmod_env"

echo "Purging modules and loading '$CONDA_MODULE' ..."
module purge
module load $CONDA_MODULE

# Activate the Conda environment
echo "Activating Conda environment '$ENV_NAME' ..."
source activate $ENV_NAME

# If the environment doesn't exist, create it and install the required packages
if [ $? -ne 0 ]; then
  echo "Conda environment '$ENV_NAME' not found. Creating it..."
  conda create -n $ENV_NAME python=3.9 -y
  source activate $ENV_NAME
  echo "Installing required packages in '$ENV_NAME' ..."
  pip install lupa packaging hpc-rocket
fi

echo "Environment setup is complete."

python collect_data.py
