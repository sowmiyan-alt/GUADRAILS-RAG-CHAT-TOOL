# GuragChat - Privacy-First Offline AI Document Assistant

A pip-installable Python package for privacy-first document analysis using local LLMs and offline embeddings.

[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3b82f6?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Offline](https://img.shields.io/badge/Mode-100%25%20Offline-76b900?style=flat-square)](#)
[![PyPI](https://img.shields.io/badge/PyPI-guragchat-0a84d8?style=flat-square)](https://pypi.org)

## Quick Start

```bash
# Install
pip install guragchat

# Use
guragchat --pdf document.pdf
```

## Features

- **100% Offline** - No cloud API calls, all processing local
- **Privacy-First** - Your data never leaves your machine
- **Easy Installation** - Single `pip install` command
- **CLI Ready** - Access via `guragchat` command
- **Multi-Format** - PDF, TXT, DOCX support
- **Safety Guardrails** - Jailbreak detection, credential protection, PII masking
- **Multi-turn Conversations** - Full chat history support
- **Fast Caching** - FAISS persistent vector store

## Installation

### From PyPI (Recommended)

```bash
pip install guragchat
```

### From Source

```bash
git clone https://github.com/sowmiyan-s/GUARDRAILS-LOCAL-RAG-WEBSITE
cd GUARDRAILS-LOCAL-RAG-WEBSITE
pip install -e .
```

## Usage

### Command Line

```bash
guragchat --pdf document.pdf
```

**Options:**
```
--pdf PATH                  Document path (required)
--model MODEL               Ollama model (default: gemma3:1b)
--ollama-host HOST          Ollama URL (default: http://localhost:11434)
--chunk-size INT            Chunk size (default: 1000)
--chunk-overlap INT         Chunk overlap (default: 200)
--sensitivity LEVEL         Data sensitivity: Public|Internal|Confidential|Restricted
--no-guardrails             Disable safety guardrails
```

**Example:**
```bash
guragchat --pdf research.pdf --model llama2 --sensitivity Confidential
```

### Python API

```python
from guragchat import build_rag_chain
from langchain_core.messages import HumanMessage

# Build RAG pipeline
db_id, rag_chain = build_rag_chain(
    ["document.pdf"],
    model="gemma3:1b",
    ollama_host="http://localhost:11434"
)

# Query
result = rag_chain.invoke({
    "input": "What is this about?",
    "chat_history": []
})

print(result["answer"])
```

## Prerequisites

### Ollama (Required)

Download from: https://ollama.ai

Start Ollama:
```bash
ollama serve
```

Download a model:
```bash
ollama pull gemma3:1b
```

Supported models: `gemma3:1b`, `llama2`, `mistral`, `neural-chat`, etc.

## Architecture

```
guragchat/
├── cli/                 # Command-line interface
├── rag/                 # RAG pipeline implementation  
├── utils/
│   ├── ollama.py       # Ollama utilities
│   └── safety.py       # Safety guardrails
└── api/                # (Future: FastAPI backend)
```

## Safety Guardrails

Four sensitivity levels:

| Level | Protection |
|-------|-----------|
| **Public** | Jailbreak detection only |
| **Internal** | + Credential & API key blocking |
| **Confidential** | + PII protection (SSN, email, card) |
| **Restricted** | + Medical, financial, HIPAA/GDPR data |

## Data Flow

```
PDF/Document → Load → Split → Embed → FAISS Store
                                         ↓
                                    Cache Disk
                                         ↓
                                    Retriever
                                         ↓
                              LLM (Ollama local)
                                         ↓
                                   Response
```

## Configuration

### .env File

```env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=gemma3:1b
DATA_SENSITIVITY=Internal
ENABLE_GUARDRAILS=true
```

## Examples

### PDF Analysis
```bash
guragchat --pdf report.pdf --sensitivity Confidential
```

### Multi-model Comparison
```bash
# Query same PDF with different models
guragchat --pdf paper.pdf --model gemma3:1b
guragchat --pdf paper.pdf --model llama2
```

### Disable Safety (Not Recommended)
```bash
guragchat --pdf document.pdf --no-guardrails
```

### Remote Ollama
```bash
guragchat --pdf doc.pdf --ollama-host http://server.local:11434
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Ollama not running" | `ollama serve` |
| "No models found" | `ollama pull gemma3:1b` |
| "ModuleNotFoundError" | `pip install --upgrade guragchat` |
| "Permission denied" | Run with `--user` or in virtual env |

## Performance Tips

- **Smaller models** (`gemma3:1b`) are faster but less accurate
- **Larger documents** benefit from smaller `--chunk-size`
- **First run** is slower (embedding generation), subsequent runs use cache
- **GPU Support**: Install `faiss-gpu` and `torch[cuda]` for GPU acceleration

## Deployment

### Docker

```dockerfile
FROM python:3.11
RUN pip install guragchat
COPY documents/ /app/docs/
WORKDIR /app
CMD ["guragchat", "--pdf", "docs/document.pdf"]
```

### Railway/Render

Create `requirements.txt`:
```
guragchat
ollama
```

Set environment variable:
```
OLLAMA_HOST=https://your-ollama-instance.com
```

## Development

```bash
# Clone
git clone https://github.com/sowmiyan-s/GUARDRAILS-LOCAL-RAG-WEBSITE
cd GUARDRAILS-LOCAL-RAG-WEBSITE

# Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e ".[dev]"

# Test
python test_installation.py
```

## Dependencies

Core:
- `langchain` - LLM orchestration
- `langchain-ollama` - Ollama integration
- `langchain-huggingface` - Embeddings
- `sentence-transformers` - Semantic embedding model
- `faiss-cpu` - Vector similarity search
- `pypdf` - PDF parsing
- `python-dotenv` - Environment config

Optional:
- `faiss-gpu` - GPU acceleration
- `torch[cuda]` - CUDA support

## API Reference

### build_rag_chain()

```python
build_rag_chain(
    file_paths: List[str],
    model: str = "gemma3:1b",
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    ollama_host: str = "http://localhost:11434",
    storage_dir: str = ".guragchat_storage"
) -> Tuple[str, Any]
```

Returns: `(db_id, rag_chain)`

### load_stored_rag_chain()

```python
load_stored_rag_chain(
    db_id: str,
    model: str = "gemma3:1b",
    ollama_host: str = "http://localhost:11434",
    storage_dir: str = ".guragchat_storage"
) -> Any
```

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

MIT - See [LICENSE](LICENSE) file

## Citation

```bibtex
@software{guragchat2024,
  title = {GuragChat: Privacy-First Offline AI Document Assistant},
  author = {Sowmiyan S},
  year = {2024},
  url = {https://github.com/sowmiyan-s/GUARDRAILS-LOCAL-RAG-WEBSITE}
}
```

## Support

- **Documentation**: [INSTALL.md](INSTALL.md)
- **Issues**: [GitHub Issues](https://github.com/sowmiyan-s/GUARDRAILS-LOCAL-RAG-WEBSITE/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sowmiyan-s/GUARDRAILS-LOCAL-RAG-WEBSITE/discussions)

## Acknowledgments

Built with:
- [LangChain](https://langchain.com) - LLM framework
- [Ollama](https://ollama.ai) - Local LLMs
- [HuggingFace](https://huggingface.co) - Transformers & embeddings
- [FAISS](https://github.com/facebookresearch/faiss) - Vector search
- [PyPDF](https://pypi.org/project/pypdf/) - PDF parsing

---

**Made with ❤️ for privacy-conscious AI enthusiasts**
