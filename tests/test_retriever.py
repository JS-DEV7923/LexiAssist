from src.retrieval.retriever import Retriever


class FakeEmbeddingProvider:
    def embed_query(self, text: str):
        return [0.1, 0.2]


class FakeVectorStore:
    def __init__(self):
        self.last_where = None

    def query(self, query_embedding, top_k, where):
        self.last_where = where
        return {
            "documents": [["chunk text"]],
            "metadatas": [[{"user_id": "u1", "doc_id": "d1", "file_name": "a.pdf", "chunk_id": 0}]],
            "distances": [[0.01]],
        }


def test_retriever_enforces_user_filter():
    store = FakeVectorStore()
    retriever = Retriever(vector_store=store, embedding_provider=FakeEmbeddingProvider())
    retriever.retrieve(user_id="u1", question="hello", top_k=5, doc_ids=None)
    assert store.last_where == {"user_id": "u1"}


def test_retriever_supports_doc_id_filter():
    store = FakeVectorStore()
    retriever = Retriever(vector_store=store, embedding_provider=FakeEmbeddingProvider())
    retriever.retrieve(user_id="u1", question="hello", top_k=5, doc_ids=["d1"])
    assert store.last_where == {"$and": [{"user_id": "u1"}, {"doc_id": {"$in": ["d1"]}}]}
