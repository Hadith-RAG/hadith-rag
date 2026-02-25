"""
LLM wrapper — shared Ollama chat interface for all agents.
Supports both streaming and non-streaming modes.
"""

import json
import re

import ollama

from config import settings


def chat_stream(
    system_prompt: str,
    user_message: str,
    model: str = None,
    print_output: bool = True,
) -> str:
    """
    Call Ollama chat with streaming. Returns the full response text.

    Args:
        system_prompt: system message for the LLM
        user_message: user message
        model: Ollama model name (defaults to settings.llm_model)
        print_output: if True, print tokens as they stream
    """
    model = model or settings.llm_model

    stream = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        stream=True,
    )

    full_response = []
    for chunk in stream:
        token = chunk.message.content
        full_response.append(token)
        if print_output:
            print(token, end="", flush=True)

    if print_output:
        print()  # newline after stream

    return "".join(full_response)


def chat(
    system_prompt: str,
    user_message: str,
    model: str = None,
) -> str:
    """
    Call Ollama chat without streaming. Returns the full response text.

    Args:
        system_prompt: system message for the LLM
        user_message: user message
        model: Ollama model name (defaults to settings.llm_model)
    """
    model = model or settings.llm_model

    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )

    return response.message.content


def chat_json(
    system_prompt: str,
    user_message: str,
    model: str = None,
) -> dict:
    """
    Call Ollama chat and parse the response as JSON.
    Falls back to extracting JSON from markdown code blocks if needed.

    Args:
        system_prompt: system message — should instruct JSON output
        user_message: user message
        model: Ollama model name (defaults to settings.small_llm_model)
    """
    model = model or settings.small_llm_model

    raw = chat(system_prompt, user_message, model=model)

    # Try direct JSON parse
    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        pass

    # Try extracting from ```json ... ``` blocks
    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Try finding any { ... } block
    match = re.search(r"\{[^{}]*\}", raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    # Fallback — return raw text wrapped
    return {"raw": raw, "error": "Could not parse JSON from LLM response"}
