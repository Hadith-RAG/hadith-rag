"""
Vector ingest — embed hadiths from data.py and store in ChromaDB.

Replaces the old store.py.

Usage:
    python -m retriever.vector.ingest
"""

import sys
from pathlib import Path

import chromadb
import ollama

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import settings
from data import hadiths


def get_embedding(text: str) -> list[float]:
    """Generate an embedding vector for the given text."""
    response = ollama.embeddings(model=settings.embedding_model, prompt=text)
    return response["embedding"]


def ingest():
    """Embed all hadiths and store them in ChromaDB."""
    client = chromadb.PersistentClient(path=settings.chroma_db_path)

    # Delete old collection if it exists (needed when changing distance metric)
    try:
        client.delete_collection("hadith_collection")
        print("Old collection deleted — recreating with cosine distance...")
    except Exception:
        pass

    # Create collection with cosine distance metric
    collection = client.get_or_create_collection(
        "hadith_collection", metadata={"hnsw:space": "cosine"}
    )

    print(f"Ingesting {len(hadiths)} hadiths into ChromaDB...")

    for i, hadith in enumerate(hadiths, 1):
        embedding = get_embedding(hadith["text"])

        collection.add(
            ids=[hadith["id"]],
            documents=[hadith["text"]],
            embeddings=[embedding],
            metadatas=[{"book": hadith["book"], "number": hadith["number"]}],
        )

        if i % 10 == 0 or i == len(hadiths):
            print(f"  [{i}/{len(hadiths)}] embedded")

    print(
        f"\nSUCCESS: {len(hadiths)} hadiths stored in ChromaDB at {settings.chroma_db_path}"
    )


if __name__ == "__main__":
    ingest()
