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

```python
from ModelManager import ModelManager

# Initialize model manager
manager = ModelManager()

# Dump models
manager.dump_models()
```

You can also execute the script directly from the command line:

```bash
python ModelManager.py [arg]
```

Replace `[arg]` with an optional argument if needed.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.