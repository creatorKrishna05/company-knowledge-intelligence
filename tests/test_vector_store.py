from domain.chunks import Chunk
from app.vector_store.base import BaseVectorStore
from app.vector_store.in_memory import InMemoryVectorStore

def test_vector_store_requires_implementation():

    class FakeVectorStore(BaseVectorStore):

        def add(self, chunk, embedding):
            pass

        def search(self, query_embedding, top_k, filters=None):
            return[]

    store = FakeVectorStore()

    assert isinstance(store, BaseVectorStore)


def test_add_and_search_returns_stored_chunk():
    store = InMemoryVectorStore()

    chunk = Chunk(
        chunk_id="Chunk-1",
        content="Company policy",
        source="policy.pdf",
        page=1,
       chunk_index=0,
    )
    embedding = [1.0, 0.0, 0.0]

    store.add(chunk, embedding)

    results = store.search(
        query_embedding=[1.0, 0.0, 0.0],
        top_k=1,
    )

    assert results[0] == chunk



def test_search_returns_most_similar_chunk():
    store = InMemoryVectorStore()

    chunk_a = Chunk("a", "AI policy", "policy.pdf", 1, 0)
    chunk_b = Chunk("b", "Leave policy", "policy.pdf", 2, 0)

    # Less similar first
    store.add(chunk_b, [0.0, 1.0, 0.0])
    store.add(chunk_a, [1.0, 0.0, 0.0])

    results = store.search(
        query_embedding=[1.0, 0.0, 0.0],
        top_k=1,
    )

    assert results[0] == chunk_a


def test_search_respects_top_k():
    store = InMemoryVectorStore()

    chunk_a = Chunk("a", "AI policy", "policy.pdf", 1, 0)
    chunk_b = Chunk("b", "Leave policy", "policy.pdf", 2, 0)
    chunk_c = Chunk("c", "Security policy", "policy.pdf", 3, 0)

    store.add(chunk_a, [1.0, 0.0, 0.0])
    store.add(chunk_b, [0.9, 0.1, 0.0])
    store.add(chunk_c, [0.0, 1.0, 0.0])

    results = store.search(
        query_embedding=[1.0, 0.0, 0.0],
        top_k=2,
    )

    assert len(results) == 2
    assert results[0] == chunk_a
    assert results[1] == chunk_b


def test_search_filters_by_source():
    store = InMemoryVectorStore()

    hr_chunk = Chunk(
        "hr-1",
        "Leave policy",
        "hr.pdf",
        1,
        0,
    )

    security_chunk = Chunk(
        "sec-1",
        "Security policy",
        "security.pdf",
        1,
        0,
    )

    store.add(hr_chunk, [1.0, 0.0, 0.0])
    store.add(security_chunk, [1.0, 0.0, 0.0])

    results = store.search(
        query_embedding=[1.0, 0.0, 0.0],
        top_k=5,
        filters={"source": "hr.pdf"},
    )

    assert results == [hr_chunk]


def test_search_empty_store_returns_empty_list():
    store = InMemoryVectorStore()

    results = store.search(
        query_embedding=[1.0, 0.0, 0.0],
        top_k=5,
    )

    assert results == []


def test_search_top_k_larger_than_available_chunks():
    store = InMemoryVectorStore()


    chunk_a = Chunk("a", "AI policy", "policy.pdf", 1, 0)
    chunk_b = Chunk("b", "Leave policy", "policy.pdf", 2, 0)

    store.add(chunk_a, [1.0, 0.0, 0.0])
    store.add(chunk_b, [0.0, 1.0, 0.0])

    results = store.search(
        query_embedding=[1.0, 0.0, 0.0],
        top_k=5,
    )

    assert len(results) == 2
    assert chunk_a in results
    assert chunk_b in results


def test_search_handles_zero_embedding():
    store = InMemoryVectorStore()

    chunk = Chunk(
        "Zero",
        "Test chunk",
        "test.pdf",
        1,
        0,
    )

    store.add(chunk, [0.0, 0.0, 0.0])

    results = store.search(
        query_embedding=[1.0, 0.0, 0.0],
        top_k=1,
    )

    assert results ==  [chunk]