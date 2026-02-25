"""
Stage 1 — Reasoning Agent

Takes the raw user query and produces a structured understanding:
- Reformulated query optimized for retrieval
- Detected intent
- Key Islamic terms extracted

Uses the small model (llama3.2:3b) for speed.
"""

from config import settings
from hadith.llm import chat_json

REASONING_SYSTEM_PROMPT = """\
You are a reasoning agent for an Islamic hadith search system.
Your job is to analyze the user's query and produce a structured understanding.

You MUST respond with valid JSON only, no other text. Use this exact format:

{
    "reformulated_query": "a clearer version of the query optimized for searching hadith texts",
    "intent": "hadith_search | general_islamic | greeting | off_topic",
    "key_terms": ["list", "of", "important", "islamic", "terms"]
}

Intent categories:
- "hadith_search": User is asking about something that could be answered by hadiths (Prophet's sayings, actions, Islamic rulings, stories of companions)
- "general_islamic": User asks about Islam generally but not specifically about hadiths
- "greeting": User is greeting, thanking, or making small talk
- "off_topic": User is asking about something completely unrelated to Islam

For the reformulated_query:
- Expand abbreviations (e.g., "PBUH" → "peace be upon him")
- Add relevant Islamic context if the query is vague
- Keep it as a clear search query, not a question

Examples:
- "hi" → {"reformulated_query": "", "intent": "greeting", "key_terms": []}
- "what about prayer" → {"reformulated_query": "hadiths about the importance and rulings of prayer salah", "intent": "hadith_search", "key_terms": ["prayer", "salah"]}
- "capital of france" → {"reformulated_query": "", "intent": "off_topic", "key_terms": []}
"""


def reason(query: str) -> dict:
    """
    Analyze the user query and return structured reasoning.

    Args:
        query: raw user input

    Returns:
        dict with keys: reformulated_query, intent, key_terms
    """
    result = chat_json(
        system_prompt=REASONING_SYSTEM_PROMPT,
        user_message=query,
        model=settings.small_llm_model,
    )

    # Ensure required keys exist with safe defaults
    return {
        "reformulated_query": result.get("reformulated_query", query),
        "intent": result.get("intent", "hadith_search"),
        "key_terms": result.get("key_terms", []),
    }
