#!/bin/bash

# This script automates the process of updating files in a Git repository after an automatic build.
# It generates new files, creates a new branch, and synchronizes specific directories with updated content.
# The script also checks if the repository exists locally, clones it if missing, and uses rsync for efficient updates.
# Optional commands for committing and pushing changes are provided but commented out for safety.

source config.env

# Paths to the new files generated by the build
IMPORTS_NEW="${IMPORTS_DIR}"
SOFTWARE_NEW="${STACKS_DIR}"
CUSTOM_NEW="${CUSTOM_DIR}"

# Paths to the existing directories in the Git repository
IMPORTS_EXISTING="${REPO_DIR}/${IMPORTS_DIR}"
SOFTWARE_EXISTING="${REPO_DIR}/${STACKS_DIR}"
CUSTOM_EXISTING="${REPO_DIR}/${CUSTOM_DIR}"

# Run the automatic build script to generate new data files
./run-hpc-rocket.sh

# Clone the repository if it does not exist locally
if [ ! -d "$REPO_DIR/.git" ]; then
    echo "Cloning repository $GITHUB_REPOSITORY"
    mkdir -p "$BUILD_DIR"
    pushd "$BUILD_DIR" || exit
    git clone git@github.com:${GITHUB_REPOSITORY}.git
    popd || exit
fi

# Switch to the repository directory, update from remote, and create/switch to a new branch
pushd "$REPO_DIR" || exit
git switch master
git pull origin master

# Check if the branch exists; create and switch to it if not
if git rev-parse --verify "$BRANCH_NAME" >/dev/null 2>&1; then
  current_branch=$(git branch --show-current)
  if [ "$current_branch" == "$BRANCH_NAME" ]; then
    echo "Already on branch '$BRANCH_NAME'."
  else
    echo "Switching to existing branch '$BRANCH_NAME'."
    git checkout "$BRANCH_NAME"
  fi
else
  echo "Creating and switching to new branch '$BRANCH_NAME'."
  git checkout -b "$BRANCH_NAME"
fi
popd || exit

# Create necessary directories if they don't exist
mkdir -p "$IMPORTS_EXISTING" "$SOFTWARE_EXISTING" "$CUSTOM_EXISTING"

# Sync new files to the corresponding directories in the Git repository
rsync -a --delete --exclude="custom/" "$IMPORTS_NEW/" "$IMPORTS_EXISTING/"   # Overwrite imports except custom
rsync -a --delete "$SOFTWARE_NEW/" "$SOFTWARE_EXISTING/"                      # Overwrite software stack
rsync -a --ignore-existing "$CUSTOM_NEW/" "$CUSTOM_EXISTING/"                 # Only add new files in custom

## Uncomment these lines to commit and push the changes to the remote repository
# pushd "$REPO_DIR"
# git add .
# git commit -m "Updated API with changes on $(date +%Y-%m-%d)"
# git push --set-upstream origin "$BRANCH_NAME"
# popd
