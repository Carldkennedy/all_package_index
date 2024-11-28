#!/bin/bash

# This script automates the process of cleaning up old files, submitting a job to SLURM,
# backing up generated data, and running a post-processing pipeline.
# The main steps include:
# - Setting up environment variables for remote server access.
# - Removing directories and files from previous runs.
# - Submitting a SLURM job using `hpc-rocket`.
# - Backing up log and pickle files to a timestamped location.
# - Running mods2docs pipeline with the specified parser and writer.
source config.env
export REMOTE_HOST
export REMOTE_USER
export DATA_DIR

# Replace placeholders in the template YAML file
envsubst < mods2docs/config.yml > hpc_rocket_config.yml

DATESTAMP="$(date +%Y%m%d-%H%M%)"                # Timestamp for backups

# Remove previous runs' directories and files to ensure a clean start
[ -d "stanage/" ] && rm -rf "stanage/"
[ -d "referenceinfo/" ] && rm -rf "referenceinfo/"
[ -f "*.log" ] && rm -f "*.log"
[ -f "*.pkl" ] && rm -f "*.pkl"

# Submit job to SLURM via hpc-rocket, using the specified configuration file
hpc-rocket launch --watch hpc_rocket_config.yml

# Run post-processing on the data returned by the SLURM job
mkdir -p data/backups/                          # Create backup directory if it doesn't exist

# Back up log and pickle files with a timestamp
for file in *.{pkl,log}; do
    cp "$file" "${file}-${DATESTAMP}.bk" && echo "Backed up $file"
done
mv data/*.bk data/backups/                     # Move backup files to the backup directory

# Run the data processing pipeline, specifying the parser and writer types
python -m mods2docs.start_pipeline --parser lmod --writer rest
