#!/bin/bash

# Run Ollama test
echo "🚀 Running Ollama test..."

# Run the test script directly since it's in the same directory
if [ -f "./4_setup_llm_test.sh" ]; then
    bash ./4_setup_llm_test.sh
    echo "✅ Ollama test completed."
else
    echo "⚠️ Ollama test script not found in the scripts directory."
fi
