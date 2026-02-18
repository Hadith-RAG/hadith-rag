# Requirements

## System Requirements

| Requirement | Version | Notes                                          |
| ----------- | ------- | ---------------------------------------------- |
| Python      | 3.10+   | Tested on Python 3.10                          |
| Ollama      | Latest  | Local LLM runtime for embeddings and inference |
| OS          | Any     | Windows / macOS / Linux                        |

## Python Packages

| Package    | Description                                         |
| ---------- | --------------------------------------------------- |
| `chromadb` | Vector database for storing and querying embeddings |
| `ollama`   | Python client for the Ollama inference engine       |

Install both with:

```bash
pip install chromadb ollama
```

## Ollama Models

This project uses two Ollama models:

| Model              | Purpose                             |
| ------------------ | ----------------------------------- |
| `nomic-embed-text` | Generates text embeddings for RAG   |
| `llama3.1:8b`      | LLM that generates the final answer |

Pull both models before running any scripts:

```bash
ollama pull nomic-embed-text
ollama pull llama3.1:8b
```

> Make sure the Ollama application is **running** before executing any Python script.

## Project Files

| File               | Description                                                                                          |
| ------------------ | ---------------------------------------------------------------------------------------------------- |
| `data.py`          | Contains 100 hadiths from Sahih al-Bukhari (pre-loaded dataset)                                      |
| `generate_data.py` | Generates `data.py` from the raw Bukhari JSON source                                                 |
| `store.py`         | Embeds all hadiths and stores them in ChromaDB                                                       |
| `search.py`        | Takes a question, retrieves relevant hadiths, generates an LLM answer, and prints referenced hadiths |
| `chroma_db/`       | Auto-generated vector database directory (gitignored)                                                |
