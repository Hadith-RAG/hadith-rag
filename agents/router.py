"""
Stage 2 — Router Agent

Decides whether the query needs hadith retrieval or a direct answer.
This replaces the old is_greeting() + SIMILARITY_THRESHOLD logic.

Uses the small model (llama3.2:3b) for speed.
"""

from config import settings
from hadith.llm import chat_json

ROUTER_SYSTEM_PROMPT = """\
You are a routing agent for an Islamic hadith search system.
Given the user's query and the reasoning analysis, decide the next action.

You MUST respond with valid JSON only, no other text. Use this exact format:

{
    "action": "retrieve" or "direct_answer",
    "reason": "brief explanation of your decision"
}

Rules:
- "retrieve": Use this when the query is about hadiths, Prophet Muhammad's teachings, Islamic rulings from hadith, stories of companions, or anything that could be answered by authentic hadith texts.
- "direct_answer": Use this when the query is a greeting, off-topic, general knowledge, or doesn't need hadith retrieval.

If the reasoning intent is "greeting" or "off_topic", ALWAYS choose "direct_answer".
If the reasoning intent is "hadith_search", ALWAYS choose "retrieve".
If the reasoning intent is "general_islamic", use your judgment — choose "retrieve" if hadiths would help, otherwise "direct_answer".
"""


def route(query: str, reasoning: dict) -> dict:
    """
    Decide whether to retrieve hadiths or answer directly.

    Args:
        query: raw user input
        reasoning: output from the reasoning agent

    Returns:
        dict with keys: action ("retrieve" | "direct_answer"), reason
    """
    user_message = (
        f"User query: {query}\n\n"
        f"Reasoning analysis:\n"
        f"- Intent: {reasoning.get('intent', 'unknown')}\n"
        f"- Reformulated query: {reasoning.get('reformulated_query', query)}\n"
        f"- Key terms: {', '.join(reasoning.get('key_terms', []))}"
    )

    result = chat_json(
        system_prompt=ROUTER_SYSTEM_PROMPT,
        user_message=user_message,
        model=settings.small_llm_model,
    )

    action = result.get("action", "retrieve")

    # Safety: validate action value
    if action not in ("retrieve", "direct_answer"):
        action = "retrieve"

    return {
        "action": action,
        "reason": result.get("reason", ""),
    }
