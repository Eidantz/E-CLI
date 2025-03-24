#!/bin/bash

# install.sh: Script to set up the virtual environment, install the package,
# configure API keys, and create an alias for the E-CLI tool.

# Step 1: Ask for the installation directory (default to current directory)
read -p "Enter installation directory (default: current directory): " install_dir
if [ -z "$install_dir" ]; then
    install_dir=$(pwd)
fi
echo "Installation directory: $install_dir"

# Step 3: Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Please install Poetry first and re-run this script."
    exit 1
fi

# Step 4: Install project dependencies using Poetry
echo "Installing dependencies with Poetry..."
poetry install

# Step 5: Build the package
echo "Building the package..."
poetry build

# Step 6: Install the package locally so that the entry point (ecli) is available
echo "Installing package locally..."
source "$install_dir/.venv/bin/activate"
pip install --no-deps dist/*.whl
if [ $? -ne 0 ]; then
    echo "Failed to install the package. Please check the output for errors."
    exit 1
fi
echo "Package installed successfully."


# Step 7: Ask for the LLM service and model selection
read -p "Enter desired LLM service (groq, openai, azure) [openai]: " llm_service
if [ -z "$llm_service" ]; then
    llm_service="openai"
fi

if [ "$llm_service" = "groq" ]; then
    default_model="llama-3.3-70b-specdec"
else
    default_model="gpt-4o"
fi

read -p "Enter desired model name (default: $default_model): " llm_model
if [ -z "$llm_model" ]; then
    llm_model="$default_model"
fi

# Step 8: Ask for API key(s) based on the selected LLM service and save them in a .env file.
echo ""
echo "=== API Key Configuration for ${llm_service} ==="
env_file="$install_dir/.env"
touch "$env_file"

if [ "$llm_service" = "groq" ]; then
    read -p "Enter your GROQ API key: " api_key
    echo "GROQ_API_KEY=\"$api_key\"" >> "$env_file"
elif [ "$llm_service" = "openai" ]; then
    read -p "Enter your OpenAI API key: " api_key
    echo "OPENAI_API_KEY=\"$api_key\"" >> "$env_file"
elif [ "$llm_service" = "azure openai" ]; then
    read -p "Enter your Azure API key (e.g. my-azure-api-key): " azure_key
    read -p "Enter your Azure API base (e.g. https://example-endpoint.openai.azure.com): " azure_base
    read -p "Enter your Azure API version (e.g. 2023-05-15): " azure_version
    echo "AZURE_API_KEY=\"$azure_key\"" >> "$env_file"
    echo "AZURE_API_BASE=\"$azure_base\"" >> "$env_file"
    echo "AZURE_API_VERSION=\"$azure_version\"" >> "$env_file"
fi

echo "API key(s) saved in $env_file"
echo ""

# Step 9: Create an alias for the ecli command in the appropriate shell rc file.
alias_line="alias ecli=\"$install_dir/.venv/bin/ecli --llm ${llm_service}/${llm_model}\""
echo "Constructed alias:"
echo "$alias_line"

if [ -f "$HOME/.zshrc" ]; then
    echo "Adding alias to $HOME/.zshrc..."
    echo "$alias_line" >> "$HOME/.zshrc"
    echo "Alias added to $HOME/.zshrc."
fi

if [ -f "$HOME/.bashrc" ]; then
    echo "Adding alias to $HOME/.bashrc..."
    echo "$alias_line" >> "$HOME/.bashrc"
    echo "Alias added to $HOME/.bashrc."
fi

echo ""
echo "Installation complete. You can now run 'ecli' from your terminal."
echo "Remember to activate the virtual environment with 'source $install_dir/.venv/bin/activate' before using the E-CLI tool."
echo "Run for example: ecli -S 'print Hello, world!'"
echo "Thank you for using the E-CLI tool!"