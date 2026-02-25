"""
VectorRetriever — ChromaDB-based semantic search.
"""

import chromadb
import ollama

from config import settings
from hadith.models import HadithRecord, HadithResult


class VectorRetriever:
    """Retrieve hadiths using ChromaDB cosine similarity search."""

    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.chroma_db_path)
        self.collection = self.client.get_collection("hadith_collection")

    def retrieve(self, query: str, top_k: int = None) -> list[HadithResult]:
        """Embed the query and find the top_k most similar hadiths."""
        top_k = top_k or settings.n_results

        # Embed the query
        response = ollama.embeddings(model=settings.embedding_model, prompt=query)
        query_embedding = response["embedding"]

        # Search ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

        # Build HadithResult list
        hadith_results = []
        for doc, meta, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            similarity = 1.0 - distance  # cosine distance → similarity

            record = HadithRecord(
                id=f"{meta.get('book', 'unknown')}_{meta.get('number', '0')}",
                text=doc,
                book=meta.get("book", "unknown"),
                number=str(meta.get("number", "")),
            )

            hadith_results.append(HadithResult(record=record, score=similarity))

        return hadith_results
