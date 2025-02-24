#!/bin/bash

# Step 1: Create and Activate Virtual Environment
if [ ! -d "GENAIENV" ]; then
    echo "Virtual environment 'GENAIENV' not found. Creating it now..."
    python -m venv GENAIENV
    echo "Virtual environment 'GENAIENV' created."
else
    echo "Virtual environment 'GENAIENV' already exists."
fi

echo "Activating virtual environment 'GENAIENV'..."
source GENAIENV/Scripts/activate

# Step 2: Install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    python -m pip install --upgrade pip
    python -m pip install --break-system-packages -r requirements.txt
else
    echo "No requirements.txt found. Skipping dependency installation."
fi
