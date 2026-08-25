from app.chunking.base import BaseChunker
from domain.documents import Document
from domain.chunks import Chunk


class FakeChunker(BaseChunker):
     
    def chunk(self, document: Document) -> list[Chunk]:
        return [
            Chunk(
                chunk_id="chunk-001",
                content=document.content,
                source=document.metadata["source"],
                page=document.metadata["page"],
                chunk_index=0,
            )
        ]


def test_chunker_returns_chunks():
    document = Document(
        content="Company leave policy.",
        metadata={
            "source": "policy.pdf",
            "page": 1,
        },
    )

    chunker = FakeChunker()

    chunks = chunker.chunk(document)

    assert isinstance(chunks, list)
    assert len(chunks) == 1
    assert isinstance(chunks[0], Chunk)