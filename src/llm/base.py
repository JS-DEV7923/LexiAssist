from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class RetrievedChunk:
    text: str
    metadata: dict
    score: float | None = None


class EmbeddingProvider(Protocol):
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        ...

    def embed_query(self, text: str) -> list[float]:
        ...


class LLMProvider(Protocol):
    def answer_with_context(self, question: str, chunks: list[RetrievedChunk]) -> str:
        ...
