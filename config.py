"""
Centralized configuration for HadithRAG.
Single load_dotenv(), all settings in one typed dataclass.
"""

from dataclasses import dataclass, field
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass
class Settings:
    # ChromaDB
    chroma_db_path: str = field(
        default_factory=lambda: os.getenv("CHROMA_DB_PATH", "./chroma_db")
    )

    # Ollama Models
    embedding_model: str = field(
        default_factory=lambda: os.getenv("EMBEDDING_MODEL", "nomic-embed-text:latest")
    )
    llm_model: str = field(
        default_factory=lambda: os.getenv("LLM_MODEL", "llama3.1:8b")
    )
    small_llm_model: str = field(
        default_factory=lambda: os.getenv("SMALL_LLM_MODEL", "llama3.2:3b")
    )

    # Search
    n_results: int = field(default_factory=lambda: int(os.getenv("N_RESULTS", "3")))


settings = Settings()
