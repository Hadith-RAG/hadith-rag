# Requirements

## System Requirements

| Requirement | Version | Notes                                          |
| ----------- | ------- | ---------------------------------------------- |
| Python      | 3.10+   | Tested on Python 3.10                          |
| Ollama      | Latest  | Local LLM runtime for embeddings and inference |
| OS          | Any     | Windows / macOS / Linux                        |

## Python Packages

| Package         | Description                                         |
| --------------- | --------------------------------------------------- |
| `chromadb`      | Vector database for storing and querying embeddings |
| `ollama`        | Python client for the Ollama inference engine       |
| `python-dotenv` | Load environment variables from `.env` file         |

Install all with:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install chromadb ollama python-dotenv
```

## Ollama Models

This project uses three Ollama models:

| Model              | Size   | Purpose                   | Used By                            |
| ------------------ | ------ | ------------------------- | ---------------------------------- |
| `nomic-embed-text` | 274 MB | Text embeddings for RAG   | Vector Retriever (ingest + search) |
| `llama3.2:3b`      | 2.0 GB | Fast structured reasoning | Reasoning Agent, Routing Agent     |
| `llama3.1:8b`      | 4.9 GB | Quality answer generation | Judge Agent, Direct Answers        |

Pull all models before running:

```bash
ollama pull nomic-embed-text
ollama pull llama3.2:3b
ollama pull llama3.1:8b
```

> Make sure the Ollama application is **running** before executing any Python script.

## Environment Variables

| Variable          | Default                   | Description                         |
| ----------------- | ------------------------- | ----------------------------------- |
| `CHROMA_DB_PATH`  | `./chroma_db`             | Path to ChromaDB storage            |
| `EMBEDDING_MODEL` | `nomic-embed-text:latest` | Ollama embedding model              |
| `LLM_MODEL`       | `llama3.1:8b`             | Large model for Judge + answers     |
| `SMALL_LLM_MODEL` | `llama3.2:3b`             | Small model for Reasoning + Routing |
| `N_RESULTS`       | `3`                       | Number of hadiths to retrieve       |

## Project Files

| File/Package | Description                                                 |
| ------------ | ----------------------------------------------------------- |
| `config.py`  | Centralized typed settings — loads all env vars once        |
| `search.py`  | CLI entry point — runs the full 3-stage agentic pipeline    |
| `data.py`    | Contains 100 hadiths from Sahih al-Bukhari                  |
| `hadith/`    | Shared kernel package — models and LLM wrappers             |
| `retriever/` | Retrieval package — vector search via ChromaDB              |
| `agents/`    | Agentic LLM pipeline — reasoning, routing, and judge agents |
| `chroma_db/` | Auto-generated vector database directory (gitignored)       |
