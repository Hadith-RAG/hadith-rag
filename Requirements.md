# Requirements

## System Requirements

| Requirement | Version    | Notes                              |
| ----------- | ---------- | ---------------------------------- |
| Python      | 3.10+      | Tested on Python 3.10              |
| Ollama      | Latest     | Local LLM runtime for embeddings   |
| OS          | Any        | Windows / macOS / Linux            |

## Python Packages

| Package    | Description                                         |
| ---------- | --------------------------------------------------- |
| `chromadb` | Vector database for storing and querying embeddings  |
| `ollama`   | Python client for the Ollama inference engine        |

Install both with:

```bash
pip install chromadb ollama
```

## Ollama Model

This project uses the **nomic-embed-text** model for generating text embeddings.

Pull the model before running any scripts:

```bash
ollama pull nomic-embed-text
```

> Make sure the Ollama application is **running** before executing any Python script.

## Project Files

| File         | Description                                                    |
| ------------ | -------------------------------------------------------------- |
| `data.py`    | Contains 100 hadiths from Sahih al-Bukhari (pre-loaded dataset)|
| `store.py`   | Embeds all hadiths and stores them in ChromaDB                 |
| `search.py`  | Accepts a query and returns semantically similar hadiths       |
| `chroma_db/` | Auto-generated vector database directory (gitignored)          |
