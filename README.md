# E-CLI (Enhanced Command-Line Interface)

**E-CLI** is an advanced command-line assistant that translates natural language queries into executable Bash/Zsh commands using large language models (LLMs). It's designed to enhance your terminal productivity by eliminating the need to memorize complex shell syntax.

---

## ✨ Features

- 🔤 Translate natural language to actual shell commands  
- 🧠 Powered by LLMs (OpenAI, Groq, Azure OpenAI, etc.)  
- 🖥️ Detects your OS and adapts command generation  
- ⚙️ Supports both "suggestion" and "execute" modes  
- 🐚 Works with Bash and Zsh  
- 🔒 API keys managed locally in `.env`  
- 💾 Session memory for command history (last 10 commands)  
- 🧹 Memory management tools  

---

## 📋 Requirements

E-CLI is built with [Poetry](https://python-poetry.org/), which requires `pipx` to install cleanly and isolate the tool.

### 🧰 Installing pipx

#### On macOS:

```bash
brew install pipx
pipx ensurepath
```

#### On Linux:

```bash
sudo apt update
sudo apt install pipx
pipx ensurepath
```

#### On other systems:

Follow the official guide:  
👉 [https://pipx.pypa.io/stable/installation/](https://pipx.pypa.io/stable/installation/)

---

### 🛠 Installing Poetry

Once `pipx` is installed, install Poetry with:

```bash
pipx install poetry
```

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/e-cli.git
cd e-cli
```

### 2. Run the install script

This sets up a virtual environment, installs dependencies, asks for your preferred LLM, and stores API keys.

```bash
bash install.sh
```

> ⚠️ Might require to run `chmod +x install.sh` to make the script executable.

> ⚠️ If you encounter issues, ensure you have the necessary permissions to execute scripts.

---

## 🛠️ Usage

Once installed, use the `ecli` command from your terminal:

### 📌 Command Flags

- `-S`, `--suggestion`: Only **suggest** the generated shell commands — nothing will be executed. *(Default if no flag is given.)*
- `-e`, `--execute`: Automatically **execute** the generated commands in Zsh.
- `-v`, `--version`: Display the current version of E-CLI.
- `--clear-memory`: Clear all session memory files.

---

## 💬 Examples

### 🔍 Just suggest a command (safe, non-destructive)

```bash
ecli -s "list all files in this directory"
```

**Output:**
```
Suggested commands:
ls -la
```

### ⚙️ Execute the command directly

```bash
ecli -e "create a new folder called projects"
```

**Output:**
```
Executing: mkdir projects
Command Output:
```

### 🧠 Use a different LLM provider/model

```bash
ecli --llm openai/gpt-4o -S "check if nginx is running"
```
> ⚠️ You will need to set up your API key in the `.env` file.
---

## 📦 Project Structure

```plaintext
e-cli/
├── pyproject.toml       # Poetry configuration
├── install.sh           # Installation & setup script
├── src/
│   └── ecli/
│       ├── __init__.py
│       └── main.py      # Main CLI logic
├── README.md
└── .env                 # API keys stored here (after setup)
```

---

## 🔐 API Key Setup

E-CLI supports multiple LLM providers. During installation, you'll be prompted to input your API key based on your selected service:

- **OpenAI** → `OPENAI_API_KEY`  
- **Groq** → `GROQ_API_KEY`  
- **Azure OpenAI** → `AZURE_API_KEY`, `AZURE_API_BASE`, `AZURE_API_VERSION`  

These are stored securely in a local `.env` file.

---

## 🤝 Contributing

Pull requests are welcome! Here's how to contribute:

1. Fork the repo  
2. Create your feature branch (`git checkout -b feature/my-awesome-feature`)  
3. Commit your changes (`git commit -m 'Add awesome feature'`)  
4. Push to the branch (`git push origin feature/my-awesome-feature`)  
5. Open a Pull Request  

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

Developed by **Eidan Tzdaka**  
Feel free to reach out or contribute ideas to enhance E-CLI!

---

## 💡 Example Queries

- `"find all Python files in this directory"`  
- `"kill the process running on port 3000"`  
- `"check if nginx is running"`  
- `"create a new git branch called dev"`  

---

> 🧠 E-CLI is your AI-powered command-line sidekick — because you have better things to do than remember shell flags.
