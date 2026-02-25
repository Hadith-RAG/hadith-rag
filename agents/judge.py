"""
Stage 3 — Judge Agent

After retrieval, validates whether the retrieved hadiths are actually
relevant to the user's query. If relevant, composes the final answer
with citations. If not, responds with "I don't have knowledge."

Uses the large model (llama3.1:8b) for answer quality.
"""

from config import settings
from hadith.llm import chat_stream
from hadith.models import HadithResult

JUDGE_SYSTEM_PROMPT = """\
You are a judge and Islamic scholar assistant for a hadith search system.

You have been given a user's question and a set of retrieved hadiths from a RAG system.

Your job is TWO-FOLD:

1. **JUDGE RELEVANCE**: Determine if the retrieved hadiths are actually relevant to the user's question. Sometimes the retrieval system returns hadiths that don't really answer the question.

2. **COMPOSE ANSWER**: 
   - If the hadiths ARE relevant: Compose a scholarly, accurate answer based strictly on the retrieved hadiths. Cite them using [Book #Number] format. Be respectful and informative.
   - If the hadiths are NOT relevant: Respond with exactly: "I don't have specific hadith knowledge on this topic. The retrieved hadiths were not relevant to your question."

Rules:
- NEVER fabricate hadiths or citations
- Base your answer STRICTLY on the provided hadiths
- Be respectful and use appropriate Islamic etiquette
- If partially relevant, use what is relevant and note limitations
"""

DIRECT_SYSTEM_PROMPT = """\
You are a helpful Islamic scholar assistant.
Respond warmly and helpfully to the user.
Do NOT fabricate or cite any hadiths — none were retrieved for this query.
Keep your response brief and relevant.
If the question is not related to Islam, politely let them know you are specialized in Islamic hadith knowledge.
"""


def judge_and_answer(
    query: str,
    results: list[HadithResult],
    print_output: bool = True,
) -> dict:
    """
    Judge retrieved hadiths for relevance and compose the final answer.

    Args:
        query: original user query
        results: retrieved HadithResult list from the retriever
        print_output: stream the answer to stdout

    Returns:
        dict with keys: answer (str), relevant (bool), citations (list)
    """
    # Build context from retrieved hadiths
    context_parts = []
    citations = []

    for i, r in enumerate(results, 1):
        ref = f"[{r.record.book} #{r.record.number}]"
        context_parts.append(f"{ref} (similarity: {r.score:.3f})\n{r.record.text}")
        citations.append(
            {
                "index": i,
                "book": r.record.book,
                "number": r.record.number,
                "text": r.record.text,
                "score": r.score,
            }
        )

    context = "\n\n".join(context_parts)

    user_message = f"Retrieved Hadiths:\n{context}\n\nUser Question: {query}"

    if print_output:
        print("\n--- LLM Answer ---\n")

    answer = chat_stream(
        system_prompt=JUDGE_SYSTEM_PROMPT,
        user_message=user_message,
        model=settings.llm_model,
        print_output=print_output,
    )

    # Determine if the answer indicates non-relevance
    relevant = "I don't have specific hadith knowledge" not in answer

    return {
        "answer": answer,
        "relevant": relevant,
        "citations": citations if relevant else [],
    }


def direct_answer(query: str, print_output: bool = True) -> str:
    """
    Answer directly without retrieval (for greetings, off-topic, etc.).

    Args:
        query: user query
        print_output: stream the answer to stdout

    Returns:
        The answer text
    """
    if print_output:
        print("\n--- LLM Answer ---\n")

    return chat_stream(
        system_prompt=DIRECT_SYSTEM_PROMPT,
        user_message=query,
        model=settings.llm_model,
        print_output=print_output,
    )
