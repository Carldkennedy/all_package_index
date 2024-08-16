#!/bin/bash

export REMOTE_HOST=stanage.shef.ac.uk
export REMOTE_USER=your_user_name

export DATESTAMP=$(date +"%Y-%m-%d")

# Submit job to SLURM
hpc-rocket launch --watch config.yml

# Wait for the job to finish
wait

# Run post-processing script on the returned data
mkdir -p results/backups/
# Backup pkl
for file in results/*; do cp "$file" "${file}-$(date +%Y%m%d).bk" && echo "Backed up $file" ; done
mv results/*.bk results/backups/

python main.py
