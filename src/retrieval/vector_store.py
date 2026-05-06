from __future__ import annotations

import chromadb
from chromadb.api.models.Collection import Collection


class ChromaVectorStore:
    def __init__(self, persist_dir: str, collection_name: str = "legal_chunks") -> None:
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection: Collection = self.client.get_or_create_collection(collection_name)

    def upsert_chunks(self, ids: list[str], embeddings: list[list[float]], documents: list[str], metadatas: list[dict]) -> None:
        self.collection.upsert(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)

    def query(self, query_embedding: list[float], top_k: int, where: dict) -> dict:
        return self.collection.query(query_embeddings=[query_embedding], n_results=top_k, where=where)

    def delete_document_chunks(self, user_id: str, doc_id: str) -> None:
        self.collection.delete(where={"$and": [{"user_id": user_id}, {"doc_id": doc_id}]})
