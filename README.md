# Local AI Agent With RAG

## Installation

**Recommended: Use a virtual environment** (installs packages locally for this project only)

### First-time setup:

1. Create a virtual environment:
```bash
python -m venv .venv
```

2. Activate it:
   - **macOS/Linux**: `source .venv/bin/activate`
   - **Windows**: `.venv\Scripts\activate`
   
   You'll see `(.venv)` in your terminal prompt when it's active.

3. Install the project and its dependencies:
```bash
pip install -e .
```

4. Download Ollama on your local machine or server based on your OS
```
[Ollama](https://ollama.com/download)
```

5. Pull models from registry
```bash
ollama pull llama3.2
```

Then
```bash
ollama pull mxbai-embed-large
```

6. Run the application
```bash
python main.py
```