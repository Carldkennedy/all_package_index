#!/bin/bash

# Ensure config.env exists
if [ ! -f config.env ]; then
    echo "Error: config.env file not found. Please ensure it exists in the current directory."
    exit 1
fi
source config.env

# Get the current commit hash (shortened to 8 characters)
CURRENT_HASH=$(git rev-parse --short=8 HEAD)

# Switch to the repository directory, update from remote, and create a new branch
pushd "$REPO_DIR" || exit

BRANCH_NAME=$(git branch --show-current)

# Set your header message
HEADER_MESSAGE="Updated API with changes on $(date +%Y-%m-%d)"

# Check if there are any changes
if git diff --quiet -- "$IMPORTS_DIR" "$STACKS_DIR"; then
   echo "No changes detected in:"
   echo $IMPORTS_DIR 
   echo $STACKS_DIR 
   echo "Skipping commit!"
   popd
   exit 0
fi

# File pattern to filter
FILE_PATTERN="*-ml-*"

# Generate a filtered diff for added modules
MODULES_ADDED=$(git diff -- "$IMPORTS_DIR" | grep -E "^\+\s*module load" | sed 's/^+\s*module load //' | tr '\n' '\n- ')
if [ -z "$MODULES_ADDED" ]; then
    MODULES_ADDED="None"
fi

# Generate a filtered diff for removed modules
MODULES_REMOVED=$(git diff -- "$IMPORTS_DIR" | grep -E "^\-\s*module load" | sed 's/^-\s*module load //' | tr '\n' '\n- ')
if [ -z "$MODULES_REMOVED" ]; then
    MODULES_REMOVED="None"
fi

# Format the body message
BODY_MESSAGE="This documentation was generated from commit $CURRENT_HASH of the all_package_index repo.

Modules added:
$MODULES_ADDED

Modules removed:
$MODULES_REMOVED"


# Show diff output for visual confirmation
echo "\nChanges to be committed:\n"
git diff 

echo $BODY_MESSAGE

read -p "Push changes to remote repository? (y/n): " CONFIRM
if [[ "$CONFIRM" != "y" ]]; then
    echo "Push aborted."
    popd
    exit 0
fi

# Commit and push the changes
git add .
git commit -m "$HEADER_MESSAGE" -m "$BODY_MESSAGE"
git push --set-upstream origin "$BRANCH_NAME" || { echo "Error: Failed to push changes."; exit 1; }

popd
