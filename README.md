# HadithRAG — Agentic Hadith Search System

A semantic search and question-answering system over **Sahih al-Bukhari** hadiths, powered by a **3-stage agentic LLM pipeline**. Ask a question in plain English — intelligent agents decide whether to retrieve hadiths, validate relevance, and compose a scholarly answer with citations.

**Stack:** Python · ChromaDB · Ollama · nomic-embed-text · llama3.2:3b · llama3.1:8b

---

## Architecture — Agentic Flow

```
USER INPUT
    │
    ▼
┌─────────────────────────────────────┐
│  Stage 1: REASONING AGENT          │
│  Model: llama3.2:3b                │
│  Job: Understand query, extract    │
│       intent, reformulate for      │
│       better retrieval             │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Stage 2: ROUTING AGENT            │
│  Model: llama3.2:3b                │
│  Job: Decide — does this query     │
│       need hadith retrieval or     │
│       a direct answer?             │
└──────────┬──────────┬───────────────┘
           │          │
     ┌─────┘          └─────┐
     ▼                      ▼
 [RETRIEVE]           [DIRECT ANSWER]
     │                      │
     ▼                      ▼
┌──────────────┐   ┌──────────────────┐
│ ChromaDB     │   │ LLM answers      │
│ Vector Search│   │ without hadiths  │
│ (top 3)      │   │ (greetings, etc) │
└──────┬───────┘   └──────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  Stage 3: JUDGE AGENT              │
│  Model: llama3.1:8b                │
│  Job: Validate retrieved hadiths   │
│       are relevant. If yes →       │
│       compose answer with          │
│       citations. If no → "I don't  │
│       have knowledge on this."     │
└─────────────────────────────────────┘
       │
       ▼
    RESPONSE
```

---

## Project Structure

```
hadith-rag/
│
├── search.py              # CLI entry point — runs the full agentic pipeline
├── config.py              # Centralized settings (all env vars in one place)
├── data.py                # 100 hadiths from Sahih al-Bukhari
├── requirements.txt       # Python dependencies
├── .env                   # Environment configuration
│
├── hadith/                # Shared kernel package
│   ├── __init__.py        # Re-exports core types
│   ├── models.py          # HadithRecord + HadithResult dataclasses
│   └── llm.py             # Ollama chat wrappers (streaming, JSON parsing)
│
├── retriever/             # Retrieval package
│   ├── __init__.py
│   └── vector/            # ChromaDB vector retriever
│       ├── __init__.py
│       ├── retriever.py   # VectorRetriever — semantic similarity search
│       └── ingest.py      # Embed hadiths → store in ChromaDB
│
├── agents/                # Agentic LLM pipeline
│   ├── __init__.py
│   ├── reasoning.py       # Stage 1 — query understanding (llama3.2:3b)
│   ├── router.py          # Stage 2 — retrieve or direct (llama3.2:3b)
│   └── judge.py           # Stage 3 — validate & answer (llama3.1:8b)
│
├── chroma_db/             # Auto-generated vector database (gitignored)
├── Requirements.md        # Full dependency documentation
├── ARCHITECTURE.md        # Deep technical guide
└── README.md              # This file
```

---

## Prerequisites

| Requirement | Version | Notes                            |
| ----------- | ------- | -------------------------------- |
| Python      | 3.10+   | Tested on Python 3.10            |
| Ollama      | Latest  | Local LLM runtime                |
| Docker      | Latest  | For sunnah.com API (data source) |

### Ollama Models

```bash
ollama pull nomic-embed-text    # Embeddings (274 MB)
ollama pull llama3.2:3b         # Reasoning + Routing agents (2.0 GB)
ollama pull llama3.1:8b         # Judge + Final answer (4.9 GB)
```

---

## Setup

### 1. Clone & Navigate

```bash
git clone <your-repo-url>
cd hadith-rag
```

### 2. Virtual Environment

```bash
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy `.example.env` to `.env` and adjust if needed:

```env
CHROMA_DB_PATH=./chroma_db
EMBEDDING_MODEL=nomic-embed-text:latest
LLM_MODEL=llama3.1:8b
SMALL_LLM_MODEL=llama3.2:3b
N_RESULTS=3
```

### 5. Ingest into ChromaDB

```bash
python -m retriever.vector.ingest
```

Expected output:

```
Ingesting 100 hadiths into ChromaDB...
  [10/100] embedded
  [20/100] embedded
  ...
SUCCESS: 100 hadiths stored in ChromaDB
```

### 6. Run Agentic Search

```bash
python search.py
```

---

## Usage Examples

### Hadith Query (Retrieves)

```
Enter your question: What did the Prophet say about prayer?

[Stage 1] Reasoning
  → Intent: hadith_search
  → Reformulated: hadiths about prayer salah importance and rulings

[Stage 2] Routing
  → Action: retrieve

[Stage 3] Retrieval
  → Found 3 hadiths (top score: 0.782)

[Stage 4] Judge & Answer
--- LLM Answer ---
Based on the retrieved hadiths, the Prophet (ﷺ) emphasized...

--- Referenced Hadiths ---
[1] bukhari | Hadith #8 (score: 0.782)
    ...
```

### Greeting (Direct Answer)

```
Enter your question: Hello!

[Stage 1] Reasoning → Intent: greeting
[Stage 2] Routing → Action: direct_answer
[Stage 3] Direct Answer

Assalamu alaikum! I'm here to help with Islamic hadith questions...
```

### Off-Topic (Direct Answer)

```
Enter your question: What is quantum physics?

[Stage 1] Reasoning → Intent: off_topic
[Stage 2] Routing → Action: direct_answer
[Stage 3] Direct Answer

I'm specialized in Islamic hadith knowledge...
```

---

## Model Strategy

| Agent                    | Model              | Size   | Purpose              |
| ------------------------ | ------------------ | ------ | -------------------- |
| Reasoning (Stage 1)      | `llama3.2:3b`      | 2.0 GB | Fast query analysis  |
| Routing (Stage 2)        | `llama3.2:3b`      | 2.0 GB | Fast classification  |
| Judge + Answer (Stage 3) | `llama3.1:8b`      | 4.9 GB | Quality final answer |
| Embeddings               | `nomic-embed-text` | 274 MB | Vector embeddings    |

---

## Notes

- `chroma_db/` is auto-generated — delete it and re-run ingest to rebuild
- Ollama must be **running** before executing any script
- The agentic pipeline makes 2–3 LLM calls per query (faster on GPU)
- `data.py` contains 100 hadiths for testing — increase `HADITH_COUNT` in `.env` for more

---

## License

This project is for educational and research purposes.
