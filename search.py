import chromadb
import ollama
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from environment variables
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text:v1.5")
LLM_MODEL = os.getenv("LLM_MODEL", "gemma3:4b")
N_RESULTS = int(os.getenv("N_RESULTS", "3"))

# Connect to ChromaDB
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_collection("hadith_collection")

# Get user query
query = input("Enter your question: ")

# Embed the query
response = ollama.embeddings(model=EMBEDDING_MODEL, prompt=query)
query_embedding = response["embedding"]

# Retrieve top relevant hadiths (3 is enough — keeps context small and fast)
results = collection.query(query_embeddings=[query_embedding], n_results=N_RESULTS)

# Collect retrieved hadiths
context_parts = []
refs = []
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    context_parts.append(f"[{meta['book']} #{meta['number']}] {doc}")
    refs.append((meta["book"], meta["number"], doc))

# Build context string for LLM
context = "\n\n".join(context_parts)

# Stream the LLM answer word-by-word
print("\n--- LLM Answer ---\n")
stream = ollama.chat(
    model=LLM_MODEL,
    messages=[
        {
            "role": "system",
            "content": (
                "You are an Islamic scholar assistant. "
                "Use the provided hadiths retrieved via RAG to answer the user's question "
                "accurately and respectfully. Base your answer strictly on the given hadiths."
            ),
        },
        {
            "role": "user",
            "content": f"Hadiths:\n{context}\n\nQuestion: {query}",
        },
    ],
    stream=True,
)

for chunk in stream:
    print(chunk.message.content, end="", flush=True)

print("\n")

# Print referenced hadiths
print("--- Referenced Hadiths ---\n")
for i, (book, number, doc) in enumerate(refs, 1):
    print(f"[{i}] {book} | Hadith #{number}")
    print(f"    {doc}")
    print()
