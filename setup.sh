#!/bin/bash

# 1. Install the package
echo -e "\n🚀 Installing OwlMind ($PROJ_VERSION)\n"
python3 -m pip install -e .

# 2. Find the bin directory
BIN_PATH=$(python3 -c "import site; import os; print(os.path.join(site.getuserbase(), 'bin'))")

# 3. Check if it's already in PATH
if [[ ":$PATH:" == *":$BIN_PATH:"* ]]; then
    echo "✅ PATH is already configured."
else
    echo "⚠️  PATH missing. Adding $BIN_PATH to ~/.zshrc..."
    echo "export PATH=\"\$PATH:$BIN_PATH\"" >> ~/.zshrc
    echo "✅ Added to ~/.zshrc. Please run 'source ~/.zshrc' to finish."
fi