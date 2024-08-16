#!/bin/bash

# # Define directories
BUILD_DIR="${HOME}/work/.build-all-package-index/"
REPO_DIR="${BUILD_DIR}/sheffield_hpc"
BRANCH_NAME="all-packages-update-$(date +%Y%m%d)"
RESULTS="results/"
IMPORTS="referenceinfo/imports/stanage/packages/"
SOFTWARE="stanage/software/stubs/"
CUSTOM="referenceinfo/imports/stanage/packages/custom/"

IMPORTS_NEW="${RESULTS}/${IMPORTS}"
IMPORTS_EXISTING="${REPO_DIR}/${IMPORTS}"
SOFTWARE_NEW="${RESULTS}/${SOFTWARE}"
SOFTWARE_EXISTING="${REPO_DIR}/${SOFTWARE}"
CUSTOM_NEW="${RESULTS}/${CUSTOM}"
CUSTOM_EXISTING="${REPO_DIR}/${CUSTOM}"

# Run automatic build to generate new files
./run.sh

# Clone the repository if it doesn't exist
if [ ! -d "$REPO_DIR/.git" ]; then
    mkdir -p "$BUILD_DIR"
    pushd "$BUILD_DIR"
    git clone git@github.com:rcgsheffield/sheffield_hpc.git
    popd
fi

pushd "$REPO_DIR"
# Pull the latest changes from the remote repository
git switch master
git pull origin master

# Create and switch to a new branch
git checkout -b "$BRANCH_NAME"
popd

mkdir -p "$IMPORTS_EXISTING" "$SOFTWARE_EXISTING" "$CUSTOM_EXISTING"

# Sync new imports to existing imports directory
rsync -a --delete "$IMPORTS_NEW/" "$IMPORTS_EXISTING/"

# Sync new software to existing software directory
rsync -a --delete "$SOFTWARE_NEW/" "$SOFTWARE_EXISTING/"

# Sync new custom to existing custom directory
rsync -a --ignore-existing "$CUSTOM_NEW/" "$CUSTOM_EXISTING/"

pushd "$REPO_DIR"
# Add changes to git
git add .

# Commit changes with a message
git commit -m "Updated files with automatic build changes on $(date +%Y-%m-%d)"

# Push the new branch to the remote repository and set upstream
git push --set-upstream origin "$BRANCH_NAME"
popd

