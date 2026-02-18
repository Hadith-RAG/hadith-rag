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

collection = client.get_or_create_collection("hadith_collection")

def get_embedding(text):
    response = ollama.embeddings(
        model=EMBEDDING_MODEL,
        prompt=text
    )
    return response["embedding"]

for hadith in hadiths:
    embedding = get_embedding(hadith["text"])

    collection.add(
        ids=[hadith["id"]],
        documents=[hadith["text"]],
        embeddings=[embedding],
        metadatas=[{
            "book": hadith["book"],
            "number": hadith["number"]
        }]
    )

print("SUCCESS: Stored in ChromaDB")
