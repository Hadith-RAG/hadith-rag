import chromadb
import ollama
from data import hadiths

# Use PersistentClient (IMPORTANT)
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection("hadith_collection")

def get_embedding(text):
    response = ollama.embeddings(
        model="nomic-embed-text",
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
