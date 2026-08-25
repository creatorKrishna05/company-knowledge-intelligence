import pytest
from app.indexing_service import IndexingService
from domain.chunks import Chunk


class FakeEmbedder:

    def embed_batch(self, texts):
        assert texts == ["chunk 1", "chunk 2"]

        return [
            [0.1, 0.2],
            [0.3, 0.4],
        ]


class FakeVectorStore:

    def __init__(self):
        self.items = []

    def add(self, chunk, embedding):
        self.items.append((chunk, embedding))


def test_indexing_service_embeds_and_stores_chunks():

    chunks = [
        Chunk(
            chunk_id="1",
            content="chunk 1",
            source="test.pdf",
            page=1,
            chunk_index=0,
        ),
        Chunk(
            chunk_id="2",
            content="chunk 2",
            source="test.pdf",
            page=1,
            chunk_index=1,
        ),
    ]

    embedder = FakeEmbedder()
    vector_store = FakeVectorStore()

    service = IndexingService(
        embedder=embedder,
        vector_store=vector_store,
    )

    service.index(chunks)

    assert vector_store.items == [
        (chunks[0], [0.1, 0.2]),
        (chunks[1], [0.3, 0.4]),
    ]


def test_indexing_service_rejects_embedding_count_mismatch():

    chunks = [
        Chunk(
            chunk_id="1",
            content="chunk 1",
            source="test.pdf",
            page=1,
            chunk_index=0,
        ),
        Chunk(
            chunk_id="2",
            content="chunk 2",
            source="test.pdf",
            page=1,
            chunk_index=1,
        ),
    ]

    class MismatchEmbedder:

        def embed_batch(self, texts):
            return [[0.1, 0.2]]

    vector_store = FakeVectorStore()

    service = IndexingService(
        embedder=MismatchEmbedder(),
        vector_store=vector_store,
    )

    with pytest.raises(ValueError, match="embedding"):
        service.index(chunks)