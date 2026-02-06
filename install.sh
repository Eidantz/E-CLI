#!/bin/bash

# install.sh: Script to set up the virtual environment, install the package,
# configure API keys, and create an alias for the E-CLI tool.

# Step 1: Ask for the installation directory (default to current directory)
read -p "Enter installation directory (default: current directory): " install_dir
if [ -z "$install_dir" ]; then
    install_dir=$(pwd)
fi
echo "Installation directory: $install_dir"

# Step 2: Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv is not installed. Please install uv first (https://docs.astral.sh/uv/) and re-run this script."
    exit 1
fi

# Step 3: Install project dependencies and create .venv using uv
echo "Installing dependencies with uv..."
uv sync --project "$install_dir"
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies. Please check the output for errors."
    exit 1
fi
echo "Package installed successfully."


# Step 7: Ask for the LLM service and model selection
read -p "Enter desired LLM service (ollama, groq, openai, azure) [ollama]: " llm_service
if [ -z "$llm_service" ]; then
    llm_service="ollama"
fi

if [ "$llm_service" = "ollama" ]; then
    default_model="glm-4.7:cloud"
elif [ "$llm_service" = "groq" ]; then
    default_model="openai/gpt-oss-120b"
elif [ "$llm_service" = "openai" ]; then
    default_model="gpt-4o"
else
    default_model="gpt-4o"
fi

read -p "Enter desired model name (default: $default_model): " llm_model
if [ -z "$llm_model" ]; then
    llm_model="$default_model"
fi

# Step 8: Ask for API key(s) / configuration based on the selected LLM service.
echo ""
env_file="$install_dir/.env"
touch "$env_file"

if [ "$llm_service" = "ollama" ]; then
    echo "=== Ollama Configuration ==="
    echo "Ollama runs locally and does not require an API key."
    read -p "Enter Ollama API base URL (default: http://localhost:11434): " ollama_base
    if [ -z "$ollama_base" ]; then
        ollama_base="http://localhost:11434"
    fi
    echo "OLLAMA_API_BASE=\"$ollama_base\"" >> "$env_file"
    echo "Ollama configuration saved in $env_file"
elif [ "$llm_service" = "groq" ]; then
    echo "=== API Key Configuration for groq ==="
    read -p "Enter your GROQ API key: " api_key
    echo "GROQ_API_KEY=\"$api_key\"" >> "$env_file"
    echo "API key saved in $env_file"
elif [ "$llm_service" = "openai" ]; then
    echo "=== API Key Configuration for openai ==="
    read -p "Enter your OpenAI API key: " api_key
    echo "OPENAI_API_KEY=\"$api_key\"" >> "$env_file"
    echo "API key saved in $env_file"
elif [ "$llm_service" = "azure" ]; then
    echo "=== API Key Configuration for azure ==="
    read -p "Enter your Azure API key (e.g. my-azure-api-key): " azure_key
    read -p "Enter your Azure API base (e.g. https://example-endpoint.openai.azure.com): " azure_base
    read -p "Enter your Azure API version (e.g. 2023-05-15): " azure_version
    echo "AZURE_API_KEY=\"$azure_key\"" >> "$env_file"
    echo "AZURE_API_BASE=\"$azure_base\"" >> "$env_file"
    echo "AZURE_API_VERSION=\"$azure_version\"" >> "$env_file"
    echo "API key(s) saved in $env_file"
fi

echo ""

# Save installation directory to .env file
echo "ECLI_INSTALL_DIR=\"$install_dir\"" >> "$env_file"
echo "Installation directory saved to $env_file"

# Step 9: Create an alias for the ecli command in the appropriate shell rc file.
# Map "ollama" to "ollama_chat" prefix required by DSPy/litellm for chat models
if [ "$llm_service" = "ollama" ]; then
    alias_prefix="ollama_chat"
else
    alias_prefix="$llm_service"
fi
alias_line="alias ecli=\"$install_dir/.venv/bin/ecli --llm ${alias_prefix}/${llm_model}\""
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
