import pytest
from domain.chunks import Chunk
from app.retrieval_service import RetrievalService


class FakeEmbedder:

    def embed(self, text: str) -> list[float]:
        return [1.0, 0.0, 0.0]


class FakeVectorStore:

    def __init__(self):
        self.received_filters = None

    def search(
        self,
        query_embedding: list[float],
        top_k: int,
        filters=None,
    ) -> list[Chunk]:

        self.received_filters = filters

        return [    
            Chunk(
                "chunk-1",
                "Leave policy",
                "hr.pdf",
                1,
                0,
            )
        ]

    


def test_retrieval_service_searches_by_query():
    embedder = FakeEmbedder()
    vector_store = FakeVectorStore()

    service = RetrievalService(
        embedder=embedder,
        vector_store=vector_store,
    )

    results = service.retrieve(
        "What is the leave policy?",
        top_k=3,
    )

    assert len(results) == 1
    assert results[0].content == "Leave policy"


def test_retrieval_forwards_filters():
    embedder = FakeEmbedder()
    vector_store = FakeVectorStore()

    service = RetrievalService(
        embedder=embedder,
        vector_store=vector_store,
    )

    service.retrieve(
        "What is the leave policy?",
        top_k=3,
        filters={"source": "hr.pdf"},
    )

    assert vector_store.received_filters == {"source": "hr.pdf"}



def test_retrieval_rejects_empty_query():
    embedder = FakeEmbedder()
    vector_store = FakeVectorStore()

    service = RetrievalService(
        embedder=embedder,
        vector_store=vector_store,
    )

    with pytest.raises(ValueError, match="query"):
        service.retrieve("", top_k=3)


def test_retrieval_rejects_invalid_top_k():
    embedder = FakeEmbedder()
    vector_store = FakeVectorStore()

    service = RetrievalService(
        embedder=embedder,
        vector_store=vector_store,
    )

    with pytest.raises(ValueError, match="top_k"):
        service.retrieve(
            "What is the leave policy?",
            top_k=0,
        )