from __future__ import annotations

from src.config.settings import Settings
from src.llm.base import EmbeddingProvider, LLMProvider
from src.llm.gemini_provider import GeminiEmbeddingProvider, GeminiLLMProvider
from src.llm.groq_provider import GroqLLMProvider
from src.llm.local_embedding_provider import LocalEmbeddingProvider


def build_providers(settings: Settings) -> tuple[EmbeddingProvider, LLMProvider]:
    if settings.embedding_provider == "gemini":
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required when EMBEDDING_PROVIDER=gemini")
        embedding_provider: EmbeddingProvider = GeminiEmbeddingProvider(
            api_key=settings.gemini_api_key, model=settings.gemini_embed_model
        )
    elif settings.embedding_provider == "local":
        embedding_provider = LocalEmbeddingProvider(model_name=settings.local_embedding_model)
    else:
        raise ValueError(f"Unsupported embedding provider: {settings.embedding_provider}")

    if settings.llm_provider == "gemini":
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required when LLM_PROVIDER=gemini")
        llm_provider: LLMProvider = GeminiLLMProvider(
            api_key=settings.gemini_api_key, model=settings.gemini_chat_model
        )
        return embedding_provider, llm_provider
    if settings.llm_provider == "groq":
        if not settings.groq_api_key:
            raise ValueError("GROQ_API_KEY is required when LLM_PROVIDER=groq")
        llm_provider = GroqLLMProvider(api_key=settings.groq_api_key, model=settings.groq_chat_model)
        return embedding_provider, llm_provider
    raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
