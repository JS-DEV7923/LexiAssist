from __future__ import annotations

import google.generativeai as genai

from src.chat.prompts import grounded_legal_prompt
from src.llm.base import EmbeddingProvider, LLMProvider, RetrievedChunk


class GeminiEmbeddingProvider(EmbeddingProvider):
    def __init__(self, api_key: str, model: str) -> None:
        genai.configure(api_key=api_key)
        self.model = model

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        for text in texts:
            result = genai.embed_content(model=self.model, content=text, task_type="retrieval_document")
            vectors.append(result["embedding"])
        return vectors

    def embed_query(self, text: str) -> list[float]:
        result = genai.embed_content(model=self.model, content=text, task_type="retrieval_query")
        return result["embedding"]


class GeminiLLMProvider(LLMProvider):
    def __init__(self, api_key: str, model: str) -> None:
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def answer_with_context(self, question: str, chunks: list[RetrievedChunk]) -> str:
        prompt = grounded_legal_prompt(question, chunks)
        response = self.model.generate_content(prompt)
        return (response.text or "").strip()
