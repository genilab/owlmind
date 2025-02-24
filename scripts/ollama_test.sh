#!/bin/bash

# Set the Ollama server URL
OLLAMA_URL="http://127.0.0.1:11434/api/generate"

# Test model name
MODEL_NAME="llama2"

# Test prompt
TEST_PROMPT="Hello, Ollama!"

# Function to test server connection
test_connection() {
    echo "Testing connection to Ollama server at $OLLAMA_URL..."

    # Send test request to Ollama server
    RESPONSE=$(curl -s -o response.json -w "%{http_code}" -X POST "$OLLAMA_URL" \
        -H "Content-Type: application/json" \
        -d "{\"model\": \"$MODEL_NAME\", \"prompt\": \"$TEST_PROMPT\", \"stream\": false}")

    # Check HTTP response code
    if [ "$RESPONSE" -eq 200 ]; then
        echo "✅ Ollama server connection successful!"
        echo "Response from server:"
        cat response.json | jq '.response' 2>/dev/null || cat response.json
    elif [ "$RESPONSE" -eq 400 ]; then
        echo "❌ Error: Bad request. Check if the model name ($MODEL_NAME) is correct."
    elif [ "$RESPONSE" -eq 404 ]; then
        echo "❌ Error: Ollama server not found. Is it running?"
    elif [ "$RESPONSE" -eq 500 ]; then
        echo "❌ Error: Server encountered an issue. Check Ollama server logs."
    else
        echo "❌ Unexpected response code: $RESPONSE"
        cat response.json
    fi

    # Clean up temporary response file
    rm -f response.json
}

# Run the test
test_connection
