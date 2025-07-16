#!/bin/bash

TARGET_DIR="./modules"

echo " Scanning for files with ':Zone.Identifier' in their names under $TARGET_DIR..."

# Find and delete files with :Zone.Identifier in the filename
find "$TARGET_DIR" -type f -name '*:Zone.Identifier*' | while read -r file; do
    echo "Deleting: $file"
    rm -f "$file"
done

echo "Cleanup complete."
