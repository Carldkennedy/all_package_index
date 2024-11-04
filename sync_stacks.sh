#!/bin/bash

# Define directories
BUILD_DIR="${HOME}/.build-all-package-index/"
REPO_DIR="${BUILD_DIR}/sheffield_hpc"
BRANCH_NAME="all-packages-update-$(date +%Y%m%d)"
IMPORTS="referenceinfo/imports/stanage/packages/"
SOFTWARE="stanage/software/stubs/"
CUSTOM="referenceinfo/imports/stanage/packages/custom/"

IMPORTS_NEW="data/${IMPORTS}"
SOFTWARE_NEW="data/${SOFTWARE}"
CUSTOM_NEW="data/${CUSTOM}"
IMPORTS_EXISTING="${REPO_DIR}/${IMPORTS}"
SOFTWARE_EXISTING="${REPO_DIR}/${SOFTWARE}"
CUSTOM_EXISTING="${REPO_DIR}/${CUSTOM}"

# Run automatic build to generate new files
./run-hpc-rocket.sh

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
# Check if the branch already exists locally
if git rev-parse --verify "$BRANCH_NAME" >/dev/null 2>&1; then
  # Check if we are already on that branch
  current_branch=$(git branch --show-current)
  if [ "$current_branch" == "$BRANCH_NAME" ]; then
    echo "Already on branch '$BRANCH_NAME'."
  else
    echo "Switching to existing branch '$BRANCH_NAME'."
    git checkout "$BRANCH_NAME"
  fi
else
  # Create and switch to the new branch
  echo "Creating and switching to new branch '$BRANCH_NAME'."
  git checkout -b "$BRANCH_NAME"
fi
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

