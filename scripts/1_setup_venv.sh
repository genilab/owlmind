#!/bin/bash

# Step 1: Detect OS and Setup Virtual Environment
ROOT_DIR="$(cd "$(dirname "$0")"/.. && pwd)"

detect_os() {
    case "$(uname -s)" in
        Linux*) OS="Linux"; CMD="python3 -m venv \"$ROOT_DIR/GENAIENV\"";;
        Darwin*) OS="Mac"; CMD="python3 -m venv \"$ROOT_DIR/GENAIENV\"";;
        CYGWIN*|MINGW*|MSYS*) OS="Windows"; CMD="python -m venv \"$ROOT_DIR/GENAIENV\"";;
        *)
            echo "Unable to detect OS. Please select:"
            echo "1) Linux"
            echo "2) Mac"
            echo "3) Windows"
            read -rp "Enter choice: " os_choice
            case $os_choice in
                1) OS="Linux"; CMD="python3 -m venv \"$ROOT_DIR/GENAIENV\"";;
                2) OS="Mac"; CMD="python3 -m venv \"$ROOT_DIR/GENAIENV\"";;
                3) OS="Windows"; CMD="python -m venv \"$ROOT_DIR/GENAIENV\"";;
                *) echo "Invalid selection. Defaulting to Linux."; OS="Linux"; CMD="python3 -m venv \"$ROOT_DIR/GENAIENV\"";;
            esac
            ;;
    esac
    echo "Detected OS: $OS"
}

# Create and activate the virtual environment in the project root
setup_virtual_env() {
    if [ ! -d "$ROOT_DIR/GENAIENV" ]; then
        echo "🚀 Creating virtual environment 'GENAIENV' in \"$ROOT_DIR\"..."
        eval "$CMD"
        if [ $? -eq 0 ]; then
            echo "✅ Virtual environment created at \"$ROOT_DIR/GENAIENV\"."
        else
            echo "❌ Failed to create virtual environment. Check permissions and Python installation."
            exit 1
        fi
    else
        echo "✅ Virtual environment already exists."
    fi
}

# Install dependencies
install_dependencies() {
    if [ -f "$ROOT_DIR/requirements.txt" ]; then
        echo "📦 Installing dependencies..."
        python -m pip install --upgrade pip
        python -m pip install --break-system-packages -r "$ROOT_DIR/requirements.txt"
    else
        echo "⚠️ requirements.txt not found. Skipping installation."
    fi
}

# Activate the virtual environment
activate_env() {
    if [[ "$OS" == "Windows" ]]; then
        source "$ROOT_DIR/GENAIENV/Scripts/activate"
    else
        source "$ROOT_DIR/GENAIENV/bin/activate"
    fi

    if [[ "$VIRTUAL_ENV" != "" ]]; then
        echo "✅ Virtual environment 'GENAIENV' activated."
    else
        echo "❌ Activation failed. Exiting."
        exit 1
    fi
}

# Execute all steps
detect_os
setup_virtual_env
activate_env
install_dependencies

echo "🎯 Virtual environment setup complete."
