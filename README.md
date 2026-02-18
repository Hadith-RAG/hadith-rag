# Hadith RAG

A semantic search system over **Sahih al-Bukhari** hadiths using text embeddings and vector similarity search. Ask a question in plain English and get the most relevant hadiths back instantly.

**Stack:** Python · ChromaDB · Ollama · nomic-embed-text

---

## Project Structure

```
hadith-rag/
├── data.py          # Dataset — 100 hadiths from Sahih al-Bukhari
├── store.py         # Step 1 — Embed hadiths and store in ChromaDB
├── search.py        # Step 2 — Search hadiths by semantic similarity
├── chroma_db/       # Auto-generated vector database (gitignored)
├── Requirements.md  # Full list of dependencies
└── README.md        # You are here
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

### 5. Set Up Ollama

1. Download and install Ollama from [ollama.com](https://ollama.com/download)
2. Start the Ollama application
3. Pull the embedding model:

```bash
ollama pull nomic-embed-text
```

> Ollama must be **running in the background** whenever you use `store.py` or `search.py`.

---

## Usage

### Step 1: Store Hadiths

Run `store.py` to embed all 100 hadiths and save them to the local ChromaDB database:

```bash
python store.py
```

**Expected output:**

```
SUCCESS: Stored in ChromaDB
```

This creates the `chroma_db/` directory with the vector index. You only need to run this **once** (or again if you update `data.py`).

### Step 2: Search Hadiths

Run `search.py` to search the stored hadiths by meaning:

```bash
python search.py
```

You will be prompted to enter a search query:

```
Enter your search query: Hadith about patience
```

The system returns the **top 10** most semantically similar hadiths:

```
Query: Hadith about patience

Results:

Hadith: Narrated Abu Said Al-Khudri ...
Book: Sahih al-Bukhari
Number: 32

---

Hadith: ...
```

You can run `search.py` as many times as you want with different queries.

---

## How It Works

```
┌──────────┐     ┌───────────┐     ┌──────────┐
│  data.py │────>│  store.py │────>│ ChromaDB │
│ 100 hadiths    │ embed via  │     │ vector   │
│          │     │ Ollama     │     │ database │
└──────────┘     └───────────┘     └────┬─────┘
                                        │
┌──────────┐     ┌───────────┐          │
│  User    │────>│ search.py │──────────┘
│  Query   │     │ embed +   │   similarity
│          │     │ search    │   search
└──────────┘     └───────────┘
```

1. **Store phase** — Each hadith text is converted into a numerical vector (embedding) using the `nomic-embed-text` model via Ollama, then stored in ChromaDB
2. **Search phase** — Your query is embedded the same way, and ChromaDB finds the hadiths whose vectors are closest in meaning

---

## Notes

- `chroma_db/` is auto-generated and included in `.gitignore` — do not commit it
- To rebuild the database, delete the `chroma_db/` folder and re-run `python store.py`
- The dataset contains the **first 100 hadiths** from Sahih al-Bukhari with full English narrator and text
- Each hadith entry in `data.py` has: `id`, `text`, `book`, and `number`

---

## License

This project is for educational and research purposes.
