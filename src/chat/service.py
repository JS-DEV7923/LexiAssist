from __future__ import annotations

import json
from pathlib import Path
import re

from src.ingestion.chunker import chunk_text
from src.ingestion.parsers import parse_uploaded_file
from src.llm.base import LLMProvider, RetrievedChunk
from src.retrieval.retriever import Retriever
from src.retrieval.vector_store import ChromaVectorStore
from src.storage.metadata_db import MetadataDB


class ChatService:
    def __init__(
        self,
        metadata_db: MetadataDB,
        vector_store: ChromaVectorStore,
        retriever: Retriever,
        llm_provider: LLMProvider,
        chunk_size: int,
        chunk_overlap: int,
        top_k: int,
        upload_dir: str,
    ) -> None:
        self.metadata_db = metadata_db
        self.vector_store = vector_store
        self.retriever = retriever
        self.llm_provider = llm_provider
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def ingest_document(self, user_id: str, file_name: str, file_bytes: bytes) -> str:
        lowered = file_name.lower()
        if not (lowered.endswith(".pdf") or lowered.endswith(".docx")):
            raise ValueError("Only PDF and DOCX files are allowed")
        text = parse_uploaded_file(file_name=file_name, file_bytes=file_bytes)
        if not text:
            raise ValueError("Could not extract text from uploaded file")
        clean_name = re.sub(r"[^a-zA-Z0-9._-]", "_", file_name)
        safe_name = f"{user_id}_{clean_name}"
        path = self.upload_dir / safe_name
        path.write_bytes(file_bytes)
        doc_id = self.metadata_db.add_document(user_id=user_id, name=file_name, path=str(path))

        chunk_records = chunk_text(text, self.chunk_size, self.chunk_overlap)
        ids = [f"{doc_id}:{item['chunk_id']}" for item in chunk_records]
        documents = [item["text"] for item in chunk_records]
        metadatas = [
            {
                "user_id": user_id,
                "doc_id": doc_id,
                "file_name": file_name,
                "chunk_id": item["chunk_id"],
                "source_span": json.dumps(item["source_span"]),
            }
            for item in chunk_records
        ]
        embeddings = self.retriever.embedding_provider.embed_texts(documents)
        self.vector_store.upsert_chunks(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)
        return doc_id

    def delete_document(self, user_id: str, doc_id: str) -> None:
        doc = self.metadata_db.get_document(user_id=user_id, doc_id=doc_id)
        if not doc:
            raise ValueError("Document not found")
        self.vector_store.delete_document_chunks(user_id=user_id, doc_id=doc_id)
        self.metadata_db.delete_document(user_id=user_id, doc_id=doc_id)
        path = Path(doc["path"])
        if path.exists():
            path.unlink()

    def ask(self, user_id: str, question: str, doc_ids: list[str] | None = None) -> dict:
        chunks = self.retriever.retrieve(user_id=user_id, question=question, top_k=self.top_k, doc_ids=doc_ids)
        if not chunks:
            answer = "I do not have enough evidence in your uploaded documents to answer that."
            citations: list[dict] = []
        else:
            answer = self.llm_provider.answer_with_context(question=question, chunks=chunks)
            if not answer:
                answer = "I do not have enough evidence in your uploaded documents to answer that."
            citations = self._build_citations(chunks)
        self.metadata_db.add_chat(
            user_id=user_id,
            question=question,
            answer=answer,
            citations_json=json.dumps(citations),
        )
        return {"answer": answer, "citations": citations, "chunks": chunks}

    def _build_citations(self, chunks: list[RetrievedChunk]) -> list[dict]:
        citations = []
        for index, chunk in enumerate(chunks, start=1):
            citations.append(
                {
                    "index": index,
                    "file_name": chunk.metadata.get("file_name", "unknown"),
                    "chunk_id": chunk.metadata.get("chunk_id"),
                    "excerpt": chunk.text[:300],
                }
            )
        return citations
