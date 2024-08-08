#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --mem=2G
#SBATCH --time=00:15:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=c.d.kennedy@sheffield.ac.uk

# # Define directories
# BUILD_DIR="${HOME}/build-all-packages/"
# REPO_DIR="${BUILD_DIR}/sheffield_hpc"
# BRANCH_NAME="all-packages-update-$(date +%Y%m%d)"

REPO_DIR="${HOME}/repos/sheffield_hpc/"
DOWNLOADS="/mnt/c/Users/cs1cdk/Downloads/lua/"
IMPORTS="referenceinfo/imports/stanage/packages/"
SOFTWARE="stanage/software/stubs/"
CUSTOM="referenceinfo/imports/stanage/packages/custom/"

## Extract new build
#tar -xzf ${DOWNLOADS}stacks.tar.gz
#wait

IMPORTS_NEW="${DOWNLOADS}/${IMPORTS}"
IMPORTS_EXISTING="${REPO_DIR}/${IMPORTS}"
mkdir -p "$IMPORTS_EXISTING"

SOFTWARE_NEW="${DOWNLOADS}/${SOFTWARE}"
SOFTWARE_EXISTING="${REPO_DIR}/${SOFTWARE}"
mkdir -p "$SOFTWARE_EXISTING"

CUSTOM_NEW="${DOWNLOADS}/${CUSTOM}"
CUSTOM_EXISTING="${REPO_DIR}/${CUSTOM}"
mkdir -p "$CUSTOM_EXISTING"

# Run automatic build to generate new files
# python build_new_stacks.py

# Clone the repository if it doesn't exist
# if [ ! -d "$REPO_DIR/.git" ]; then
#     mkdir -p "$BUILD_DIR"
#     pushd "$BUILD_DIR"
#     git clone git@github.com:rcgsheffield/sheffield_hpc.git
#     popd
# fi
# 
# pushd "$REPO_DIR"
# # Pull the latest changes from the remote repository
# git switch master
# git pull origin master
# 
# # Create and switch to a new branch
# git checkout -b "$BRANCH_NAME"
# popd

# Sync new imports to existing imports directory
rsync -a --delete "$IMPORTS_NEW/" "$IMPORTS_EXISTING/"

# Sync new software to existing software directory
rsync -a --delete "$SOFTWARE_NEW/" "$SOFTWARE_EXISTING/"

# Sync new custom to existing custom directory
rsync -a --ignore-existing "$CUSTOM_NEW/" "$CUSTOM_EXISTING/"

# pushd "$REPO_DIR"
# # Add changes to git
# git add .
# 
# # Commit changes with a message
# git commit -m "Updated files with automatic build changes on $(date +%Y-%m-%d)"
# 
# # Push the new branch to the remote repository and set upstream
# git push --set-upstream origin "$BRANCH_NAME"
# popd

