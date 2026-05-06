from __future__ import annotations

from src.llm.base import EmbeddingProvider, RetrievedChunk
from src.retrieval.vector_store import ChromaVectorStore


class Retriever:
    def __init__(self, vector_store: ChromaVectorStore, embedding_provider: EmbeddingProvider) -> None:
        self.vector_store = vector_store
        self.embedding_provider = embedding_provider

    def retrieve(self, user_id: str, question: str, top_k: int, doc_ids: list[str] | None = None) -> list[RetrievedChunk]:
        query_embedding = self.embedding_provider.embed_query(question)
        where = {"user_id": user_id}
        if doc_ids:
            where = {"$and": [{"user_id": user_id}, {"doc_id": {"$in": doc_ids}}]}
        result = self.vector_store.query(query_embedding=query_embedding, top_k=top_k, where=where)

        docs = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]
        chunks: list[RetrievedChunk] = []
        for idx, doc in enumerate(docs):
            chunks.append(
                RetrievedChunk(
                    text=doc,
                    metadata=metadatas[idx] if idx < len(metadatas) else {},
                    score=distances[idx] if idx < len(distances) else None,
                )
            )
        return chunks
