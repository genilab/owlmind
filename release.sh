#!/bin/bash
####
# Generic Python Release Script with Module-Based Validation
#

set -e
PROJ_NAME=$(grep -m 1 '^name = ' pyproject.toml | cut -d '"' -f 2)
PROJ_VERSION=$(grep -m 1 '^version = ' pyproject.toml | cut -d '"' -f 2)

DIST_DIR="dist"
TESTS_DIR="tests"
CONFIG_FILE=".pypirc"

echo "---------------------------------------------------------"
echo " PROJECT:  $PROJ_NAME"
echo " VERSION:  $PROJ_VERSION"
echo "---------------------------------------------------------"
echo " " 


###
### CODE VALIDATION
###

echo -e "1. Validation test..."

TEST_PATH="$TESTS_DIR/$PROJ_NAME"
if [ ! -d "$TEST_PATH" ] && [ -d "$PROJ_NAME/$TESTS_DIR" ]; then
    TEST_PATH="$PROJ_NAME/$TESTS_DIR"
fi

if [ -d "$TEST_PATH" ]; then
    echo "... executing tests (python -m $PROJ_NAME.tests)"
    python3 -m "$PROJ_NAME.tests"
    echo "✅ Validation successful."
fi
echo -e "👍 Done!\n" 

###
### CLEANUP
###

echo -e "2. Cleaning workspace..."

rm -rf "$DIST_DIR" build/ *.egg-info
echo -e "👍 Done!\n" 

###
### BUILD DISTRIBUTION
###

echo -e "3. Building distributions..."

python3 -m build --no-isolation &> /dev/null
echo -e "👍 Done!\n" 

###
### PACKAGE HEALTH
###

echo -e "4. Checking package health..."

python3 -m twine check "$DIST_DIR"/*
echo -e "👍 Done!\n" 

###
### RELEASE
###


if [[ "$1" == "--release" ]]; then
    echo -e "5. Releasing package..."
    
    if [ -f "$CONFIG_FILE" ]; then
        echo "... using local credentials from $CONFIG_FILE"
        python3 -m twine upload --config-file "$CONFIG_FILE" "$DIST_DIR"/*
    else
        echo "... manual login required ($CONFIG_FILE not found)"
        python3 -m twine upload "$DIST_DIR"/*
    fi
    echo -e "\n\n ✅ Success! $PROJ_NAME v$PROJ_VERSION is live."
else
    echo -e "\n\n✅ Checked! $PROJ_NAME v$PROJ_VERSION is ready (use --release)."
fi