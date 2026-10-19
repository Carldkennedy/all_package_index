#!/bin/bash

set -e

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

# Submit job to SLURM via hpc-rocket, using the specified configuration file
if hpc-rocket launch --watch hpc_rocket_config.yml; then
    :
else
    status=$?
    echo "Error: HPC-Rocket failed; documentation generation stopped." >&2
    exit "$status"
fi

# Preserve the previous documentation until remote collection succeeds.
if [ -d "${STACKS}/" ]; then rm -rf "${STACKS}/"; fi
if [ -d "${IMPORTS}/" ]; then rm -rf "${IMPORTS}/"; fi

# Run post-processing on the data returned by the SLURM job
mkdir -p ${DATA_DIR}/backups/                          # Create backup directory if it doesn't exist

# Back up log and pickle files with a timestamp
for file in "${DATA_DIR}"/*.{pkl,log}; do
    [ -f "$file" ] || continue
    cp "$file" "${DATA_DIR}/backups/$(basename "$file")-${DATESTAMP}.bk"
    echo "Backed up ${file}"
done

# Run the data processing pipeline, specifying the parser and writer types
python -m mods2docs.start_pipeline --parser lmod --writer rest
