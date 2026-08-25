import pytest
from domain.documents import Document
from app.chunking.recursive_chunker import RecursiveChunker


def test_recursive_chunker_configuration():
    chunker = RecursiveChunker(500, 100)

    assert chunker.chunk_size == 500
    assert chunker.overlap == 100

def test_recursive_chunker_rejects_zero_chunk_size():
    with pytest.raises(ValueError):
        RecursiveChunker(0, 100)

def test_recursive_chunker_rejects_negative_overlap():
    with pytest.raises(ValueError):
        RecursiveChunker(500, -1)


def test_recursive_chunker_rejects_overlap_equal_to_chunk_size():
    with pytest.raises(ValueError):
        RecursiveChunker(500, 500)


def test_recursive_chunker_returns_one_chunk_for_small_document():
    document = Document(
        content="Company leave policy.",
        metadata={
            "source": "policy.pdf",
            "page": 1,
        },
    )

    chunker = RecursiveChunker(100, 20)

    chunks = chunker.chunk(document)

    assert len(chunks) == 1

def test_recursive_chunker_splits_large_document():
    document = Document(
        content="0123456789ABCDEFGHIJ",
        metadata={
            "source": "policy.pdf",
            "page": 1,
        },
    )

    chunker = RecursiveChunker(10, 2)

    chunks = chunker.chunk(document)

    assert len(chunks) > 1


def test_recursive_chunker_preserves_chunk_size():
    document = Document(
        content="0123456789ABCDEFGHIJ",
        metadata={
            "source": "policy.pdf",
            "page": 1,
        },
    )

    chunker = RecursiveChunker(10, 2)

    chunks = chunker.chunk(document)

    assert len(chunks[0].content) == 10

def test_recursive_chunker_applies_overlap():
    document = Document(
        content="0123456789ABCDEFGHIJ",
        metadata={
            "source": "policy.pdf",
            "page": 1,
        },
    ) 

    chunker = RecursiveChunker(10, 2)

    chunks = chunker.chunk(document)

    assert chunks[0].content[-2:] == chunks[1].content[:2]


def test_recursive_chunker_assigns_sequential_chunk_indexes():
    document = Document(
        content="0123456789ABCDEFGHIJ",
        metadata={
            "source": "policy.pdf",
            "page": 1,
        },
    )

    chunker = RecursiveChunker(10, 2)

    chunks = chunker.chunk(document)

    assert [chunk.chunk_index for chunk in chunks] == [0, 1]


def test_recursive_chunker_generates_unique_chunk_ids():
    document = Document(
        content="0123456789ABCDEFGHIJ",
        metadata={
            "source": "policy.pdf",
            "page": 1,
        },
    )

    chunker = RecursiveChunker(10, 2)

    chunks = chunker.chunk(document)

    chunk_ids = [chunk.chunk_id for chunk in chunks]

    assert len(chunk_ids) == len(set(chunk_ids))


def test_recursive_chunker_generates_deterministic_chunk_ids():
    document = Document(
        content="0123456789ABCDEFGHIJ",
        metadata={
            "source": "policy.pdf",
            "page": 1,
        },
    )

    chunker = RecursiveChunker(10, 2)

    chunks = chunker.chunk(document)

    assert chunks[0].chunk_id == "policy.pdf:1:0"
    assert chunks[1].chunk_id == "policy.pdf:1:1"

def test_recursive_chunker_preserves_paragraph_boundaries():
    document = Document(
        content="Paragraph one.\n\nParagraph two.",
        metadata={"source": "test.txt", "page": 1},
    )

    chunker = RecursiveChunker(chunk_size=100, overlap=0)

    chunks = chunker.chunk(document)

    assert len(chunks) == 2
    assert chunks[0].content == "Paragraph one."
    assert chunks[1].content == "Paragraph two."

def test_recursive_chunker_splits_on_paragraph_separator():
    chunker = RecursiveChunker(chunk_size=100, overlap=0)

    text = "Paragraph one.\n\nParagraph two."

    pieces = chunker._split_text(text, "\n\n")

    assert pieces == [
        "Paragraph one.",
        "Paragraph two.",
    ]

def test_recursive_chunker_recursively_splits_using_separator_hierarchy():
    chunker = RecursiveChunker(chunk_size=20, overlap=0)

    text = "Paragraph A.\n\nParagraph B."

    separators = ["\n\n", "\n", " ", ""]

    pieces = chunker._recursive_split(text, separators)

    assert pieces == [
        "Paragraph A.",
        "Paragraph B.",
    ]


def test_recursive_chunker_uses_next_separator_when_piece_is_too_large():
    chunker = RecursiveChunker(chunk_size=20, overlap=0)

    text = "This is a very long paragraph that needs splitting."

    separators = ["\n\n", "\n", " ", ""]

    pieces = chunker._recursive_split(text, separators)

    assert all(len(piece) <= 20 for piece in pieces)

def test_recursive_chunker_recurses_when_split_piece_is_too_large():
    chunker = RecursiveChunker(chunk_size=20, overlap=0)

    text = "Short paragraph.\n\nThis is a very long paragraph that needs splitting."

    separators = ["\n\n", "\n", " ", ""]

    pieces = chunker._recursive_split(text, separators)

    assert all(len(piece) <= 20 for piece in pieces)

def test_recursive_chunker_uses_character_fallback():
    chunker = RecursiveChunker(chunk_size=10, overlap=0)

    text = "abcdefghijklmnop"

    separators = ["\n\n", "\n", " ", ""]

    pieces = chunker._recursive_split(text, separators)

    assert all(len(piece) <= 10 for piece in pieces)


def test_recursive_chunker_creates_chunks_from_recursive_pieces():
    document = Document(
        content="Paragraph one.\n\nParagraph two.",
        metadata={"source": "test.txt", "page": 1},
    )

    chunker = RecursiveChunker(chunk_size=100, overlap=0)

    chunks = chunker.chunk(document)

    assert [chunk.content for chunk in chunks] == [
        "Paragraph one.",
        "Paragraph two.",
    ]


def test_recursive_chunker_applies_overlap_between_chunks():
    document = Document(
        content="0123456789ABCDEFGHIJ",
        metadata={"source": "policy.pdf", "page": 1},
    )

    chunker = RecursiveChunker(10, 2)

    chunks = chunker.chunk(document)

    assert chunks[0].content[-2:] == chunks[1].content[:2]