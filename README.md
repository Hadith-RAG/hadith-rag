# Hadith RAG

A semantic search and question-answering system over **Sahih al-Bukhari** hadiths. Ask a question in plain English — the system retrieves the most relevant hadiths and uses a local LLM to compose a grounded, scholarly answer.

**Stack:** Python · ChromaDB · Ollama · nomic-embed-text · llama3.1:8b

---

## Project Structure

```
hadith-rag/
├── data.py            # Dataset — 100 hadiths from Sahih al-Bukhari
├── generate_data.py   # Generates data.py from the raw Bukhari JSON
├── store.py           # Step 1 — Embed hadiths and store in ChromaDB
├── search.py          # Step 2 — Ask a question, get an LLM answer + references
├── chroma_db/         # Auto-generated vector database (gitignored)
├── Requirements.md    # Full list of dependencies
└── README.md          # You are here
```

---

## Prerequisites

Before starting, make sure you have the following installed:

- **Python 3.10+** — [Download Python](https://www.python.org/downloads/)
- **Ollama** — [Download Ollama](https://ollama.com/download)

See [Requirements.md](Requirements.md) for the complete dependency list.

---

## Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd hadith-rag
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows (PowerShell):**

```powershell
.\venv\Scripts\activate
```

**Windows (CMD):**

```cmd
venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

> You should see `(venv)` at the beginning of your terminal prompt.

### 4. Install Python Dependencies

```bash
pip install chromadb ollama
```

### 5. Set Up Ollama Models

1. Download and install Ollama from [ollama.com](https://ollama.com/download)
2. Start the Ollama application
3. Pull both required models:

```bash
ollama pull nomic-embed-text
ollama pull llama3.1:8b
```

> Ollama must be **running in the background** whenever you use `store.py` or `search.py`.

---

## Usage

### Step 1: Store Hadiths

Run `store.py` once to embed all 100 hadiths and save them to the local ChromaDB database:

```bash
python store.py
```

**Expected output:**

```
SUCCESS: Stored in ChromaDB
```

You only need to run this **once** (or again if you update `data.py`).

### Step 2: Ask a Question

Run `search.py` to ask a question and get an LLM-generated answer:

```bash
python search.py
```

You will be prompted to enter a question:

```
Enter your question: What does Islam say about good deeds?
```

**Example output:**

```
--- LLM Answer ---

Based on the hadiths provided, Islam places great emphasis on good deeds...
[Streamed word-by-word as the model generates]

--- Referenced Hadiths ---

[1] Sahih al-Bukhari | Hadith #28
    Narrated Abu Huraira: The Prophet said, "To feed (the poor)..."

[2] Sahih al-Bukhari | Hadith #43
    Narrated 'Aisha: ...the best deed in the sight of Allah is that which is done regularly.

[3] Sahih al-Bukhari | Hadith #59
    ...
```

---

## How It Works

```
┌──────────┐     ┌───────────┐     ┌──────────────┐
│  data.py │────>│  store.py │────>│   ChromaDB   │
│ 100 hadiths    │ embed via  │     │ vector store │
│          │     │ nomic-embed│     └──────┬───────┘
└──────────┘     └───────────┘            │
                                          │ similarity search
┌──────────┐     ┌───────────┐            │
│  User    │────>│ search.py │────────────┘
│ Question │     │ embed +   │
│          │     │ retrieve  │────> llama3.1:8b
└──────────┘     └───────────┘           │
                                         ▼
                              ┌─────────────────────┐
                              │   LLM Answer        │
                              │   (streamed live)   │
                              ├─────────────────────┤
                              │  Referenced Hadiths │
                              │  [1] Book | #N      │
                              └─────────────────────┘
```

1. **Store phase** — Each hadith is converted into a vector embedding using `nomic-embed-text` via Ollama, then stored in ChromaDB
2. **Search phase** — Your question is embedded the same way; ChromaDB finds the top 3 most semantically similar hadiths
3. **Answer phase** — The retrieved hadiths + your question are sent to `llama3.1:8b` with a system prompt; the answer streams live to your terminal
4. **References** — The 3 source hadiths are printed at the end so every claim is traceable

---

## Notes

- `chroma_db/` is auto-generated and included in `.gitignore` — do not commit it
- To rebuild the database, delete the `chroma_db/` folder and re-run `python store.py`
- The dataset contains the **first 100 hadiths** from Sahih al-Bukhari with full English narrator and text
- The LLM answer streams word-by-word — first output appears within a few seconds
- Generation time depends on your hardware (CPU: ~1–3 min, GPU: much faster)

---

## License

This project is for educational and research purposes.
