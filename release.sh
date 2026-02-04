#!/bin/bash
# Generic Python Release Script with Module-Based Validation
#

set -euo pipefail

DIST_DIR="dist"
TESTS_DIR="tests"
CONFIG_FILE=".pypirc"

###
# PROJECT METADATA
###

PROJ_NAME=$(grep -m 1 '^name = ' pyproject.toml | cut -d '"' -f 2)

PROJ_VERSION=$(python3 - <<EOF
import sys
sys.path.insert(0, 'src')
import $PROJ_NAME
print($PROJ_NAME.__version__)
EOF
)

###
# ARGUMENT PARSING
###

DO_INCREMENT=false
DO_RELEASE=false

for arg in "$@"; do
    case "$arg" in
        --increment) DO_INCREMENT=true ;;
        --release)   DO_RELEASE=true ;;
        *) echo "❌ Unknown argument: $arg"; exit 1 ;;
    esac
done

if $DO_INCREMENT && ! $DO_RELEASE; then
    echo "❌ --increment can only be used together with --release"
    exit 1
fi

echo -e "\n🚀 Releasing Process: $PROJ_NAME ($PROJ_VERSION)\n"

###
# VALIDATION
###

echo "1. Validation test..."

TEST_PATH="$TESTS_DIR/$PROJ_NAME"
if [ ! -d "$TEST_PATH" ] && [ -d "$PROJ_NAME/$TESTS_DIR" ]; then
    TEST_PATH="$PROJ_NAME/$TESTS_DIR"
fi

if [ -d "$TEST_PATH" ]; then
    python3 -m "$PROJ_NAME.tests"
    echo "✅ Validation successful."
else
    echo "⚠️  No tests found, skipping."
fi
echo

###
# CLEANUP
###

echo "2. Cleaning workspace..."

find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.py[co]" -delete 2>/dev/null || true
find . -name ".pytest_cache" -type d -exec rm -rf {} +
find . -name ".coverage" -delete 2>/dev/null || true
rm -rf "$DIST_DIR" build/ *.egg-info .eggs/

echo "✅ Done!"
echo

###
# VERSION INCREMENT (ONLY HERE, BEFORE BUILD)
###

if $DO_RELEASE && $DO_INCREMENT; then
    echo "3. Incrementing version..."

    IFS='.' read -r MAJOR MINOR PATCH <<< "$PROJ_VERSION"
    [[ -z "$MAJOR" || -z "$MINOR" || -z "$PATCH" ]] && {
        echo "❌ Invalid version format: $PROJ_VERSION"
        exit 1
    }

    NEW_VERSION="${MAJOR}.${MINOR}.$((PATCH + 1))"

    VERSION_FILE=$(python3 - <<EOF
import inspect, $PROJ_NAME
print(inspect.getfile($PROJ_NAME))
EOF
)

    sed -i.bak \
        -E "s/__version__ *= *['\"][^'\"]+['\"]/__version__ = \"$NEW_VERSION\"/" \
        "$VERSION_FILE"
    rm -f "${VERSION_FILE}.bak"

    PROJ_VERSION="$NEW_VERSION"
    echo "✅ Version bumped to $PROJ_VERSION"
    echo
fi

###
# BUILD (quiet)
###

echo "4. Building distributions..."
python3 -m build --no-isolation &> /dev/null
echo "✅ Done!"
echo

###
# PACKAGE HEALTH (quiet)
###

echo "5. Checking package health..."
python3 -m twine check "$DIST_DIR"/* &> /dev/null
echo "✅ Done!"
echo

###
# RELEASE
###

if $DO_RELEASE; then
    echo "6. Releasing package..."

    if [ -f "$CONFIG_FILE" ]; then
        python3 -m twine upload --config-file "$CONFIG_FILE" "$DIST_DIR"/*
    else
        python3 -m twine upload "$DIST_DIR"/*
    fi

    echo -e "\n🎉 SUCCESS!! $PROJ_NAME v$PROJ_VERSION is live."
else
    echo -e "\n🎉 CHECKED!! $PROJ_NAME v$PROJ_VERSION is ready (use --release)."
fi
