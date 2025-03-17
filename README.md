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

You can execute the script directly from the command line:

```bash
python ModelManager.py
```

The script can be executed with or without an argument. If an argument is provided, it should be the name of the model you want to manage. For example:

```bash
python ModelManager.py deepseek-coder-base
```

This will manage the specified model. If no argument is provided, the script will manage all models.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.