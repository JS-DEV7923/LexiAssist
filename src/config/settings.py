from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    llm_provider: str
    embedding_provider: str
    gemini_api_key: str
    gemini_chat_model: str
    gemini_embed_model: str
    groq_api_key: str
    groq_chat_model: str
    local_embedding_model: str
    chroma_persist_dir: str
    metadata_db_path: str
    upload_dir: str
    max_upload_mb: int
    chunk_size: int
    chunk_overlap: int
    retrieval_top_k: int


def load_settings() -> Settings:
    load_dotenv()
    return Settings(
        llm_provider=os.getenv("LLM_PROVIDER", "gemini"),
        embedding_provider=os.getenv("EMBEDDING_PROVIDER", "gemini"),
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
        gemini_chat_model=os.getenv("GEMINI_CHAT_MODEL", "gemini-1.5-flash"),
        gemini_embed_model=os.getenv("GEMINI_EMBED_MODEL", "models/embedding-001"),
        groq_api_key=os.getenv("GROQ_API_KEY", ""),
        groq_chat_model=os.getenv("GROQ_CHAT_MODEL", "llama-3.1-8b-instant"),
        local_embedding_model=os.getenv("LOCAL_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"),
        chroma_persist_dir=os.getenv("CHROMA_PERSIST_DIR", "data/chroma"),
        metadata_db_path=os.getenv("METADATA_DB_PATH", "data/sqlite/metadata.db"),
        upload_dir=os.getenv("UPLOAD_DIR", "data/uploads"),
        max_upload_mb=int(os.getenv("MAX_UPLOAD_MB", "25")),
        chunk_size=int(os.getenv("CHUNK_SIZE", "800")),
        chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "120")),
        retrieval_top_k=int(os.getenv("RETRIEVAL_TOP_K", "5")),
    )
