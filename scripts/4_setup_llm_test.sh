#!/bin/bash

# Set .env file location
ROOT_DIR="$(cd "$(dirname "$0")"/.. && pwd)"
ENV_FILE="$ROOT_DIR/.env"

# Check if .env file exists
if [[ ! -f "$ENV_FILE" ]]; then
    echo "⚠️ .env file not found. Run setup first."
    exit 1
fi

# Load environment variables from .env
export $(grep -v '^#' "$ENV_FILE" | xargs)

# Validate required environment variables
if [[ -z "$SERVER_URL" ]]; then
    echo "⚠️ SERVER_URL not set in .env. Please configure your environment."
    exit 1
fi

# Set test parameters
MODEL_NAME="${SERVER_MODEL:-llama2}"
TEST_PROMPT="Hello, Ollama!"

# Function to test server connection
test_connection() {
    local url=$1
    local api_key=$2
    echo "🔍 Testing server: $url"

    # Prepare the curl command based on the presence of an API key
    if [[ -n "$api_key" ]]; then
        RESPONSE=$(curl -s -o response.json -w "%{http_code}" -X POST "$url/api/generate" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $api_key" \
            -d "{\"model\": \"$MODEL_NAME\", \"prompt\": \"$TEST_PROMPT\", \"stream\": false}")
    else
        RESPONSE=$(curl -s -o response.json -w "%{http_code}" -X POST "$url/api/generate" \
            -H "Content-Type: application/json" \
            -d "{\"model\": \"$MODEL_NAME\", \"prompt\": \"$TEST_PROMPT\", \"stream\": false}")
    fi

    # Check the response
    if [[ "$RESPONSE" -eq 200 ]]; then
        echo "✅ Success! Response: $(cat response.json)"
    else
        echo "❌ Failed with code $RESPONSE"
    fi

    # Cleanup response file
    rm -f response.json
}

# Menu loop for repeated tests
while true; do
    echo -e "\n🎛️ Select a test to run:"
    echo "1) Test Local Ollama"
    echo "2) Test FAU HPC Server"
    echo "3) Test Both"
    echo "4) Exit"

    read -rp "Enter choice (1/2/3/4): " choice

    case "$choice" in
        1) 
            test_connection "http://localhost:11434" ""
            ;;
        2) 
            if [[ -z "$SERVER_API_KEY" ]]; then
                echo "⚠️ No API key found. Please reconfigure your FAU setup."
            else
                test_connection "$SERVER_URL" "$SERVER_API_KEY"
            fi
            ;;
        3) 
            test_connection "http://localhost:11434" ""
            if [[ -n "$SERVER_API_KEY" ]]; then
                test_connection "$SERVER_URL" "$SERVER_API_KEY"
            else
                echo "⚠️ No API key found. Skipping FAU server test."
            fi
            ;;
        4) 
            echo "🚪 Exiting test suite."
            exit 0
            ;;
        *) 
            echo "❌ Invalid choice. Please enter 1, 2, 3, or 4."
            ;;
    esac

    # Ask user if they want to run another test
    read -rp "🔄 Run another test? (y/n): " cont
    if [[ "$cont" =~ ^[Nn]$ ]]; then
        echo "🚪 Exiting test suite."
        exit 0
    fi
done

echo "🎯 Testing completed."
