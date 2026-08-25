from domain.chunks import Chunk

def test_chunk_creation():
    chunk = Chunk(
        chunk_id = "chunk- 001",
        content = "Company leave policy allows 20 days of annual leave.",
        source = "Company_knowledge_test.pdf",
        page = 2,
        chunk_index = 0,
    )

    assert chunk.chunk_id == "chunk- 001"
    assert chunk.content == "Company leave policy allows 20 days of annual leave."
    assert chunk.page == 2
    assert chunk.chunk_index == 0 