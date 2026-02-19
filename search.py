import chromadb
import ollama
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from environment variables
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text:latest")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.1:8b")
N_RESULTS = int(os.getenv("N_RESULTS", "3"))
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.5"))

# --- Layer 1: Keyword Intent Classifier ---
GREETING_PATTERNS = [
    "hello",
    "hi",
    "hey",
    "salam",
    "assalamu",
    "greetings",
    "good morning",
    "good evening",
    "good night",
    "how are you",
    "thank you",
    "thanks",
    "bye",
    "goodbye",
    "who are you",
    "what can you do",
    "what are you",
]


def is_greeting(query: str) -> bool:
    """Return True if the query is a greeting or off-topic pleasantry."""
    q = query.lower().strip()
    return any(q.startswith(p) or q == p for p in GREETING_PATTERNS)


# Connect to ChromaDB
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_collection("hadith_collection")

# Get user query
query = input("Enter your question: ")

# --- Check Layer 1 first (no embedding cost) ---
if is_greeting(query):
    retrieval_relevant = False
    refs = []
    print("\n--- LLM Answer ---\n")
    stream = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful Islamic scholar assistant. "
                    "Respond warmly and helpfully to the user. "
                    "Do NOT fabricate or cite any hadiths — none were retrieved for this query."
                ),
            },
            {
                "role": "user",
                "content": query,
            },
        ],
        stream=True,
    )
    for chunk in stream:
        print(chunk.message.content, end="", flush=True)
    print("\n")

else:
    # Embed the query
    response = ollama.embeddings(model=EMBEDDING_MODEL, prompt=query)
    query_embedding = response["embedding"]

    # Retrieve top relevant hadiths
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=N_RESULTS,
        include=["documents", "metadatas", "distances"],
    )

    # --- Layer 2: Similarity Threshold Check ---
    # ChromaDB cosine distance = 1 - cosine_similarity (range: 0.0 to 2.0)
    # So: cosine_similarity = 1 - cosine_distance (range: 0.0 to 1.0)
    top_distance = results["distances"][0][0]
    top_similarity = 1.0 - top_distance  # Correct cosine inversion

    retrieval_relevant = top_similarity >= SIMILARITY_THRESHOLD

    if retrieval_relevant:
        # Build context from retrieved hadiths
        context_parts = []
        refs = []
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            context_parts.append(f"[{meta['book']} #{meta['number']}] {doc}")
            refs.append((meta["book"], meta["number"], doc))

        context = "\n\n".join(context_parts)

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

    else:
        # Low relevance — answer without hadiths
        refs = []
        print("\n--- LLM Answer ---\n")
        stream = ollama.chat(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful Islamic scholar assistant. "
                        "Answer the user's question based on your general knowledge. "
                        "Do NOT fabricate or cite any specific hadiths — none were relevant enough to retrieve."
                    ),
                },
                {
                    "role": "user",
                    "content": query,
                },
            ],
            stream=True,
        )
        for chunk in stream:
            print(chunk.message.content, end="", flush=True)
        print("\n")
        print(
            f"(No hadiths retrieved — top cosine similarity: {top_similarity:.3f}, threshold: {SIMILARITY_THRESHOLD})\n"
        )

# Print referenced hadiths only when relevant
if refs:
    print("--- Referenced Hadiths ---\n")
    for i, (book, number, doc) in enumerate(refs, 1):
        print(f"[{i}] {book} | Hadith #{number}")
        print(f"    {doc}")
        print()
