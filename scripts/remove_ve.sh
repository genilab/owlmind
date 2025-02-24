#!/bin/bash

# Set the root directory to the script's parent directory (project root)
ROOT_DIR="$(cd "$(dirname "$0")"/.. && pwd)"
VENV_DIR="$ROOT_DIR/GENAIENV"

# Confirm with the user before proceeding
echo "This will permanently delete the virtual environment at: $VENV_DIR"
read -rp "Are you sure you want to proceed? (y/n): " confirm

if [[ $confirm =~ ^[Yy]$ ]]; then
    # Kill any Python processes using the environment
    echo "🔍 Checking for active Python processes related to GENAIENV..."
    pkill -f "$VENV_DIR" 2>/dev/null

    # Check if the directory exists
    if [ -d "$VENV_DIR" ]; then
        echo "⚠️ Stopping any VSCode/terminal processes accessing the environment..."
        
        # Forcefully remove the directory
        echo "🧹 Removing virtual environment directory: $VENV_DIR"
        rm -rf "$VENV_DIR"

        # Double-check removal
        if [ ! -d "$VENV_DIR" ]; then
            echo "✅ Virtual environment 'GENAIENV' has been successfully removed."
        else
            echo "❌ Failed to remove the environment. Retrying with elevated privileges..."
            sudo rm -rf "$VENV_DIR"
            
            if [ ! -d "$VENV_DIR" ]; then
                echo "✅ Virtual environment 'GENAIENV' removed successfully with elevated privileges."
            else
                echo "❌ Could not remove the directory even with sudo. Please check permissions manually."
            fi
        fi
    else
        echo "⚠️ Virtual environment directory '$VENV_DIR' does not exist."
    fi
else
    echo "Operation cancelled. Virtual environment '$VENV_DIR' remains intact."
fi
