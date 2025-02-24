#!/bin/bash

# Main Startup Script for GENAIENV Project
SCRIPTS_DIR="./scripts"

# Check if virtual environment exists
if [ -d "GENAIENV" ]; then
    echo "🟢 Virtual environment 'GENAIENV' detected."
    echo "What would you like to do?"
    echo "1) Set up environment configuration"
    echo "2) Update environment configuration and test LLM servers"
    echo "3) Remove 'GENAIENV' environment"
    echo "4) Run LLM tests"
    read -rp "Enter your choice (1/2/3/4): " env_choice

    case $env_choice in
        1)
            echo "🔧 Running environment configuration setup..."
            cd "$SCRIPTS_DIR" || exit
            bash 2_setup_env.sh
            cd - > /dev/null
            ;;
        2)
            echo "🔄 Updating environment configuration and running tests..."
            cd "$SCRIPTS_DIR" || exit
            bash 2_setup_env.sh
            bash 4_setup_llm_test.sh  # Automatically runs tests after reconfig
            cd - > /dev/null
            ;;
        3)
            echo "🛑 Removing virtual environment..."
            cd "$SCRIPTS_DIR" || exit
            bash remove_ve.sh
            cd - > /dev/null

            # After removal, ask if we should reinstall
            read -rp "Would you like to reinstall the environment? (y/n): " reinstall_choice
            if [[ "$reinstall_choice" =~ ^[Yy]$ ]]; then
                echo "🔄 Reinstalling environment..."
                cd "$SCRIPTS_DIR" || exit
                bash 1_setup_venv.sh
                bash 2_setup_env.sh
                bash 3_setup_ollama.sh
                bash 4_setup_llm_test.sh
                cd - > /dev/null
            else
                echo "👋 Exiting after environment removal."
            fi
            ;;
        4)
            echo "🚀 Running LLM tests..."
            cd "$SCRIPTS_DIR" || exit
            bash 4_setup_llm_test.sh
            cd - > /dev/null
            ;;
        *)
            echo "⚠️ Invalid choice. Exiting."
            exit 1
            ;;
    esac
else
    echo "🔍 No virtual environment detected. Starting full setup process..."

    # Step 1: Set up the virtual environment
    cd "$SCRIPTS_DIR" || exit
    bash 1_setup_venv.sh
    bash 2_setup_env.sh
    bash 3_setup_ollama.sh
    bash 4_setup_llm_test.sh
    cd - > /dev/null

    echo "🎯 Setup complete. Follow the instructions in the README for next steps."
fi
