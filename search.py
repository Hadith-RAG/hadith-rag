"""
HadithRAG — Agentic Search CLI

3-stage LLM pipeline:
  Stage 1: Reasoning   (llama3.2:3b)  — query understanding
  Stage 2: Routing     (llama3.2:3b)  — retrieve or direct answer
  Stage 3: Judge       (llama3.1:8b)  — validate & compose answer

Usage:
    python search.py
"""

import sys
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import settings
from agents.reasoning import reason
from agents.router import route
from agents.judge import judge_and_answer, direct_answer
from retriever.vector.retriever import VectorRetriever


def print_header():
    """Print the application header."""
    print("=" * 60)
    print("  HadithRAG — Agentic Search")
    print(f"  Models: {settings.small_llm_model} (reasoning/routing)")
    print(f"          {settings.llm_model} (judge/answer)")
    print("=" * 60)
    print()


def print_stage(stage_num: int, name: str, detail: str = ""):
    """Print a stage indicator."""
    print(f"\n[Stage {stage_num}] {name}")
    if detail:
        print(f"  → {detail}")


def print_references(citations: list[dict]):
    """Print referenced hadiths."""
    if not citations:
        return

    print("\n--- Referenced Hadiths ---\n")
    for c in citations:
        print(
            f"[{c['index']}] {c['book']} | Hadith #{c['number']} (score: {c['score']:.3f})"
        )
        # Truncate long texts for display
        text = c["text"]
        if len(text) > 200:
            text = text[:200] + "..."
        print(f"    {text}")
        print()


def main():
    """Main entry point — runs the agentic search pipeline."""
    print_header()

    query = input("Enter your question: ").strip()
    if not query:
        print("No query provided. Exiting.")
        return

    # ─── Stage 1: Reasoning ───────────────────────────────────
    print_stage(1, "Reasoning", f"Analyzing query with {settings.small_llm_model}...")
    reasoning = reason(query)
    print(f"  Intent: {reasoning['intent']}")
    print(f"  Reformulated: {reasoning['reformulated_query']}")
    print(f"  Key terms: {', '.join(reasoning['key_terms'])}")

    # ─── Stage 2: Routing ─────────────────────────────────────
    print_stage(2, "Routing", f"Deciding action with {settings.small_llm_model}...")
    routing = route(query, reasoning)
    print(f"  Action: {routing['action']}")
    print(f"  Reason: {routing['reason']}")

    # ─── Branch: Direct Answer ────────────────────────────────
    if routing["action"] == "direct_answer":
        print_stage(3, "Direct Answer", f"Responding with {settings.llm_model}...")
        direct_answer(query)
        print()
        return

    # ─── Branch: Retrieve + Judge ─────────────────────────────
    print_stage(3, "Retrieval", "Searching ChromaDB...")
    retriever = VectorRetriever()
    search_query = reasoning.get("reformulated_query") or query
    results = retriever.retrieve(search_query)
    print(f"  Found {len(results)} hadiths (top score: {results[0].score:.3f})")

    # ─── Stage 4: Judge ───────────────────────────────────────
    print_stage(
        4, "Judge & Answer", f"Validating relevance with {settings.llm_model}..."
    )
    judgment = judge_and_answer(query, results)

    # Print references if relevant
    print_references(judgment.get("citations", []))

    print()


if __name__ == "__main__":
    main()
