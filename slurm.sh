#!/bin/bash
#SBATCH --time=00:15:00              # Set a maximum job run time of 15 minutes
#SBATCH --mem=1G                      # Request 1 GB of memory
#SBATCH --job-name=API-collect-data   # Job name for identification
#SBATCH --output=slurm.out            # Output file for SLURM job logs

# This script runs a data collection process using the `mods2docs` package in a Conda environment.
# It performs the following steps:
# - Loads the Anaconda module to use Conda environments
# - Activates the '$ENV_NAME' environment; if it doesn’t exist, the script creates it and installs dependencies
# - Sets up a designated data folder and runs the `collect_data` module in `mods2docs` with the `lmod` parser
source config.env

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
  eval "$INSTALL_REQUIRED_PACKAGES"
fi

echo "Environment setup is complete."

# Create the data folder if it doesn't already exist
mkdir -p $DATA_DIR

# Run the data collection script with the specified parser
python -m mods2docs.collect_data --parser lmod
