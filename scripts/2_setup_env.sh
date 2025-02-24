#!/bin/bash

# Configure Prompt Engineering Lab with .env setup
ROOT_DIR="$(cd "$(dirname "$0")"/.. && pwd)"
EXAMPLE_ENV_FILE="$ROOT_DIR/.env_example"

if [[ ! -f "$EXAMPLE_ENV_FILE" ]]; then
    echo "⚠️ No '.env_example' found in root directory. Please ensure it exists."
    exit 1
fi

ENV_FILE="$ROOT_DIR/.env"

# Check if .env already exists
if [[ -f "$ENV_FILE" ]]; then
    read -rp ".env already exists. Replace it with new settings? (y/n): " replace_env
    if [[ ! $replace_env =~ ^[Yy]$ ]]; then
        echo "🛑 Keeping existing .env."
        exit 0
    fi
    rm -f "$ENV_FILE"
fi

# Copy the template env file
cp "$EXAMPLE_ENV_FILE" "$ENV_FILE"
echo "✅ Created .env file from .env_example."

# Prompt for server selection
echo -e "\nSelect the Ollama server type:"
echo "1) Local Ollama (localhost)"
echo "2) FAU HPC Server"
read -rp "Enter your choice (1/2): " server_choice

# Update the .env based on the selection
if [[ "$server_choice" == "1" ]]; then
    # Configure for Local Ollama
    awk '{gsub(/^#SERVER_TYPE=ollama/, "SERVER_TYPE=ollama"); gsub(/^#SERVER_URL=http:\/\/localhost:11434/, "SERVER_URL=http://localhost:11434"); gsub(/^SERVER_TYPE=open-webui/, "#SERVER_TYPE=open-webui"); gsub(/^SERVER_URL=https:\/\/chat.hpc.fau.edu/, "#SERVER_URL=https://chat.hpc.fau.edu"); gsub(/^SERVER_API_KEY=.*/, "#SERVER_API_KEY="); print}' "$ENV_FILE" > tmpfile && mv tmpfile "$ENV_FILE"
    echo "✅ Configuration updated for Local Ollama."

elif [[ "$server_choice" == "2" ]]; then
    # Configure for FAU Server
    awk '{gsub(/^SERVER_TYPE=ollama/, "#SERVER_TYPE=ollama"); gsub(/^SERVER_URL=http:\/\/localhost:11434/, "#SERVER_URL=http://localhost:11434"); gsub(/^#SERVER_TYPE=open-webui/, "SERVER_TYPE=open-webui"); gsub(/^#SERVER_URL=https:\/\/chat.hpc.fau.edu/, "SERVER_URL=https://chat.hpc.fau.edu"); print}' "$ENV_FILE" > tmpfile && mv tmpfile "$ENV_FILE"

    # Ask for the API key
    while true; do
        read -rp "Do you have an FAU API key? (y/n): " api_choice
        if [[ "$api_choice" =~ ^[Nn]$ ]]; then
            echo "📖 Please refer to 'docs/CONFIG-FAU.md' to get your API key."
            read -rp "Press Enter once you have the key..."
        fi

        read -rp "Enter your FAU API key: " api_key
        if [[ -n "$api_key" ]]; then
            # Ensure SERVER_API_KEY line exists and update it
            if grep -q '^#SERVER_API_KEY=' "$ENV_FILE"; then
                awk -v key="$api_key" '{gsub(/^#SERVER_API_KEY=.*/, "SERVER_API_KEY="key); print}' "$ENV_FILE" > tmpfile && mv tmpfile "$ENV_FILE"
            else
                echo "SERVER_API_KEY=$api_key" >> "$ENV_FILE"
            fi
            echo "✅ FAU configuration updated with the provided API key."
            break
        else
            echo "⚠️ No API key entered. Please try again."
        fi
    done

else
    echo "❌ Invalid selection. Defaulting to Local Ollama."
    awk '{gsub(/^#SERVER_TYPE=ollama/, "SERVER_TYPE=ollama"); gsub(/^#SERVER_URL=http:\/\/localhost:11434/, "SERVER_URL=http://localhost:11434"); gsub(/^SERVER_TYPE=open-webui/, "#SERVER_TYPE=open-webui"); gsub(/^SERVER_URL=https:\/\/chat.hpc.fau.edu/, "#SERVER_URL=https://chat.hpc.fau.edu"); gsub(/^SERVER_API_KEY=.*/, "#SERVER_API_KEY="); print}' "$ENV_FILE" > tmpfile && mv tmpfile "$ENV_FILE"
    echo "✅ Defaulted to Local Ollama."
fi

# Fetch and display available Ollama models
echo -e "\n🔍 Fetching available Ollama models..."
if command -v ollama &> /dev/null; then
    echo "Available models:"
    ollama list | awk '{print "- " $1}'
else
    echo "⚠️ Ollama CLI not found. Please ensure Ollama is installed."
    echo "📖 Refer to the installation guide for instructions."
fi

# Prompt for model type selection
echo -e "\nChoose one of the active models from the list above."
read -rp "Enter the model type: " model_type
if [[ -n "$model_type" ]]; then
    if grep -q '^#SERVER_MODEL=' "$ENV_FILE"; then
        awk -v model="$model_type" '{gsub(/^#SERVER_MODEL=.*/, "SERVER_MODEL="model); print}' "$ENV_FILE" > tmpfile && mv tmpfile "$ENV_FILE"
    else
        echo "SERVER_MODEL=$model_type" >> "$ENV_FILE"
    fi
    echo "✅ Model type set to '$model_type'."
else
    echo "⚠️ No model type entered. Keeping default settings."
fi

# Prompt for Discord token setup
echo -e "\nHave you set up your Discord bot token?"
read -rp "Do you have a Discord token ready? (y/n): " discord_choice

if [[ "$discord_choice" =~ ^[Yy]$ ]]; then
    read -rp "Enter your Discord token: " discord_token
    if [[ -n "$discord_token" ]]; then
        if grep -q '^#DISCORD_TOKEN=' "$ENV_FILE"; then
            awk -v token="$discord_token" '{gsub(/^#DISCORD_TOKEN=.*/, "DISCORD_TOKEN="token); print}' "$ENV_FILE" > tmpfile && mv tmpfile "$ENV_FILE"
        else
            echo "DISCORD_TOKEN=$discord_token" >> "$ENV_FILE"
        fi
        echo "✅ Discord token saved in .env."
    else
        echo "⚠️ No token entered. Please manually update your .env file."
    fi
else
    echo "📖 Please refer to 'INSTALLING.md' to set up your Discord bot and manually enter the token in the .env file."
fi

echo "🎯 Configuration completed successfully."

# Show final .env file state
echo -e "\n🔍 Final .env configuration:"
cat "$ENV_FILE"

# Ask if the user wants to test the new configuration
read -rp "Would you like to test the new configuration now? (y/n): " run_test

if [[ "$run_test" =~ ^[Yy]$ ]]; then
    bash "$ROOT_DIR/scripts/4_setup_llm_test.sh"
else
    echo "🟢 Configuration complete. Environment is ready for use."
    # Activate environment
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        source "$ROOT_DIR/GENAIENV/Scripts/activate"
    else
        source "$ROOT_DIR/GENAIENV/bin/activate"
    fi
    echo "✅ Virtual environment 'GENAIENV' activated. Follow the README instructions for usage."
fi
