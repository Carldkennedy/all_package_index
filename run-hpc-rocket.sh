#!/bin/bash

export REMOTE_HOST=stanage.shef.ac.uk
export REMOTE_USER=cs1cdk
export DATESTAMP=$(date +"%Y-%m-%d")

# Remove previous runs dirs and files
[ -d "stanage/" ] && rm -rf "stanage/"
[ -d "referenceinfo/" ] && rm -rf "referenceinfo/"
[ -f "*.log" ] && rm -f "*.log"
[ -f "*.pkl" ] && rm -f "*.pkl"

# Submit job to SLURM
hpc-rocket launch --watch mods2docs/config.yml

# Run post-processing script on the returned data
mkdir -p data/backups/
# Backup pkl
for file in *.{pkl,log}; do cp "$file" "${file}-$(date +%Y%m%d).bk" && echo "Backed up $file" ; done
mv data/*.bk data/backups/

python -m mods2docs.start_pipeline --parser lmod --writer rest
