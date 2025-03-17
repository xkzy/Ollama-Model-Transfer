# Ollama Model Dumper

A Python utility for managing and dumping Ollama models.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/xkzy/Ollama-Model-Transfer.git
   ```
2. Navigate to the project directory:
   ```bash
   cd ollama-model-dumper
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

You can execute the script directly from the command line with the following commands:

### Backup all models
```bash
python ModelManager.py backup
```

### Export a specific model
```bash
python ModelManager.py export deepseek-coder-base
```

### Import models from a backup folder
```bash
python ModelManager.py import /path/to/backup/folder
```

If no arguments are provided, the script will prompt you with an interactive menu to choose an action.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.