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
HEADER_MESSAGE="Update All Package Index via mods2docs on $(date +%Y-%m-%d)"

# Check if there are any changes
if git diff --quiet -- "$IMPORTS_DIR" "$STACKS_DIR" && [ -z "$(git ls-files --others --exclude-standard "$IMPORTS_DIR" "$STACKS_DIR")" ]; then
   echo "No changes detected in:"
   echo $IMPORTS_DIR 
   echo $STACKS_DIR 
   echo "Skipping commit!"
   popd
   exit 0
fi

# File pattern to filter
FILE_PATTERN="*-ml-*"

# Capture added and removed modules from tracked files that match the pattern
MODULES_ADDED=$(git diff -- "$IMPORTS_DIR" -- "$FILE_PATTERN" | grep -E "^\+\s*module load" | sed 's/^+\s*module load //')
MODULES_REMOVED=$(git diff -- "$IMPORTS_DIR" -- "$FILE_PATTERN" | grep -E "^\-\s*module load" | sed 's/^-\s*module load //')

# Capture added modules from untracked files that match the pattern
UNTRACKED_FILES=$(git ls-files --others --exclude-standard "$IMPORTS_DIR" | grep -E "$FILE_PATTERN")

for file in $UNTRACKED_FILES; do
    NEW_MODULES=$(grep -E "^\s*module load" "$file" | sed 's/^\s*module load //')
    if [ -n "$NEW_MODULES" ]; then
        MODULES_ADDED="${MODULES_ADDED}
$NEW_MODULES"
    fi
done

# Remove empty lines, sort the modules, and remove duplicates
MODULES_ADDED=$(echo "$MODULES_ADDED" | sort -u | sed '/^$/d')
MODULES_REMOVED=$(echo "$MODULES_REMOVED" | sort -u | sed '/^$/d')

# Ensure non-empty values for commit message
MODULES_ADDED=${MODULES_ADDED:-"None"}
MODULES_REMOVED=${MODULES_REMOVED:-"None"}

# Format the commit message with proper line breaks
BODY_MESSAGE="This documentation was generated from commit $CURRENT_HASH of the all_package_index repo.

Modules added:
$(echo "$MODULES_ADDED" | awk '{print "- "$0}')

Modules removed:
$(echo "$MODULES_REMOVED" | awk '{print "- "$0}')"


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
