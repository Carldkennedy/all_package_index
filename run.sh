#!/bin/bash

export REMOTE_HOST=stanage.shef.ac.uk
export REMOTE_USER=your_user_name

export DATESTAMP=$(date +"%Y-%m-%d")

# Submit job to SLURM
hpc-rocket launch --watch config.yml

# Wait for the job to finish
wait

# Run post-processing script on the returned data

# Backup pkl
for file in results/*.{pkl,out}; do cp "$file" "backups/${file}-$(date +%Y%m%d).bk" && echo "Backed up $file" ; done


