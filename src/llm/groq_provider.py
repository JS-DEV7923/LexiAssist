from __future__ import annotations

from groq import Groq

from src.chat.prompts import grounded_legal_prompt
from src.llm.base import LLMProvider, RetrievedChunk


class GroqLLMProvider(LLMProvider):
    def __init__(self, api_key: str, model: str) -> None:
        self.client = Groq(api_key=api_key)
        self.model = model

    def answer_with_context(self, question: str, chunks: list[RetrievedChunk]) -> str:
        prompt = grounded_legal_prompt(question, chunks)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a legal QA assistant grounded on provided context."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
        )
        return (response.choices[0].message.content or "").strip()
