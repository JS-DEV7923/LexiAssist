from __future__ import annotations

from src.llm.base import RetrievedChunk


def grounded_legal_prompt(question: str, chunks: list[RetrievedChunk]) -> str:
    context_lines = []
    for idx, chunk in enumerate(chunks, start=1):
        name = chunk.metadata.get("file_name", "unknown")
        chunk_id = chunk.metadata.get("chunk_id", "n/a")
        context_lines.append(f"[{idx}] doc={name} chunk={chunk_id}\n{chunk.text}")
    context = "\n\n".join(context_lines)
    return (
        "You are a legal document QA assistant. "
        "Answer only from the provided context. "
        "If evidence is insufficient, say so explicitly.\n\n"
        f"Question: {question}\n\n"
        "Context:\n"
        f"{context}\n\n"
        "Return a concise answer and cite sources as [1], [2], ... matching context blocks."
    )
