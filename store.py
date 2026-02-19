import chromadb
import ollama
from data import hadiths
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from environment variables
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text:v1.5")

# Use PersistentClient (IMPORTANT)
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

# Delete old collection if it exists (needed when changing distance metric)
try:
    client.delete_collection("hadith_collection")
    print("Old collection deleted — recreating with cosine distance...")
except Exception:
    pass

# Cosine distance is the correct metric for semantic similarity on sentence embeddings.
# ChromaDB stores cosine distance = 1 - cosine_similarity (range: 0.0 to 2.0)
collection = client.get_or_create_collection(
    "hadith_collection", metadata={"hnsw:space": "cosine"}
)


def get_embedding(text):
    response = ollama.embeddings(model=EMBEDDING_MODEL, prompt=text)
    return response["embedding"]


for hadith in hadiths:
    embedding = get_embedding(hadith["text"])

    collection.add(
        ids=[hadith["id"]],
        documents=[hadith["text"]],
        embeddings=[embedding],
        metadatas=[{"book": hadith["book"], "number": hadith["number"]}],
    )

print("SUCCESS: Stored in ChromaDB")
