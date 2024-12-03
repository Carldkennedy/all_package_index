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

STACKS="${STACKS_DIR%%/*}" # xtract the top-level directory
IMPORTS="${IMPORTS_DIR%%/*}" # xtract the top-level directory

# Replace placeholders in the template YAML file
envsubst < mods2docs/config.yml > hpc_rocket_config.yml

DATESTAMP="$(date +%Y%m%d-%H%M)"                # Timestamp for backups

# Remove previous runs' directories and files to ensure a clean start
[ -d "${STACKS}/" ] && rm -rf "${STACKS}/"
[ -d "${IMPORTS}/" ] && rm -rf "${IMPORTS}/"
[ -f "${DATA_DIR}/*.log" ] && rm -f "${DATA_DIR}/*.log"
[ -f "${DATA_DIR}/*.pkl" ] && rm -f "${DATA_DIR}/*.pkl"

# Submit job to SLURM via hpc-rocket, using the specified configuration file
hpc-rocket launch --watch hpc_rocket_config.yml

# Run post-processing on the data returned by the SLURM job
mkdir -p ${DATA_DIR}/backups/                          # Create backup directory if it doesn't exist

# Back up log and pickle files with a timestamp
for file in ${DATA_DIR}/*.{pkl,log}; do
    cp "${file}" "${file}-${DATESTAMP}.bk" && echo "Backed up ${file}"
    mv ${DATA_DIR}/*bk ${DATA_DIR}/backups/
done

# Run the data processing pipeline, specifying the parser and writer types
python -m mods2docs.start_pipeline --parser lmod --writer rest
