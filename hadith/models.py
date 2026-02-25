"""Typed data models for HadithRAG."""

from dataclasses import dataclass


@dataclass
class HadithRecord:
    """A single hadith record."""

    id: str  # e.g. "bukhari_1"
    text: str  # English body text
    book: str  # e.g. "Sahih al-Bukhari"
    number: str  # hadith number


@dataclass
class HadithResult:
    """A retrieval result wrapping a HadithRecord with its score."""

    record: HadithRecord
    score: float  # cosine similarity (0.0–1.0)
