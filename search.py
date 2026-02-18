import chromadb
import ollama

# Connect to SAME ChromaDB folder
client = chromadb.PersistentClient(path="./chroma_db")

# Load collection
collection = client.get_collection("hadith_collection")

# Query text
query = input("Enter your search query: ")

# Create embedding
response = ollama.embeddings(
    model="nomic-embed-text",
    prompt=query
)

query_embedding = response["embedding"]

# Search
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=10
)

# Print results
print("\nQuery:", query)
print("\nResults:\n")

for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print("Hadith:", doc)
    print("Book:", meta["book"])
    print("Number:", meta["number"])
    print("\n---\n")
