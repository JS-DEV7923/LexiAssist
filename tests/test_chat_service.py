from src.chat.service import ChatService
from src.retrieval.retriever import Retriever
from src.storage.metadata_db import MetadataDB


class DummyEmbeddingProvider:
    def embed_texts(self, texts):
        return [[0.1, 0.2] for _ in texts]

    def embed_query(self, text):
        return [0.1, 0.2]


class DummyVectorStore:
    def __init__(self):
        self.deleted = None
        self.upserted = 0

    def upsert_chunks(self, ids, embeddings, documents, metadatas):
        self.upserted = len(ids)

    def query(self, query_embedding, top_k, where):
        return {"documents": [[]], "metadatas": [[]], "distances": [[]]}

    def delete_document_chunks(self, user_id, doc_id):
        self.deleted = (user_id, doc_id)


class DummyLLM:
    def answer_with_context(self, question, chunks):
        return "answer"


def test_chat_service_fallback_on_no_chunks(tmp_path):
    db = MetadataDB(str(tmp_path / "metadata.db"))
    retriever = Retriever(DummyVectorStore(), DummyEmbeddingProvider())
    service = ChatService(
        metadata_db=db,
        vector_store=retriever.vector_store,
        retriever=retriever,
        llm_provider=DummyLLM(),
        chunk_size=100,
        chunk_overlap=10,
        top_k=3,
        upload_dir=str(tmp_path / "uploads"),
    )
    user_id = db.create_user("u@example.com", "x")
    result = service.ask(user_id=user_id, question="What is this?")
    assert "enough evidence" in result["answer"]
