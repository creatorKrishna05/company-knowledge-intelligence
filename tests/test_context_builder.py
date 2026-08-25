from domain.chunks import Chunk
from app.context_builder import ContextBuilder


def test_context_builder_formats_chunks():
    chunks = [
        Chunk(
            "chunk-1",
            "Employees get 20 days leave.",
            "hr.pdf",
            1,
            0,
        ),
    ]

    builder = ContextBuilder()

    context = builder.build(chunks)

    assert "Employees get 20 days leave." in context
    assert "hr.pdf" in context
    assert "Page: 1" in context

def test_context_builder_preserves_chunk_order():
    chunks = [
        Chunk(
            "chunk-1",
            "First policy information.",
            "hr.pdf",
            1,
            0,
        ),
        Chunk(
            "chunk-2",
            "Second policy information.",
            "hr.pdf",
            2,
            1,
        ),
    ]

    builder = ContextBuilder()

    context = builder.build(chunks)

    first_position = context.index("First policy information.")
    second_position = context.index("Second policy information.")

    assert first_position < second_position


def test_context_builder_empty_chunks_returns_empty_string():
    builder = ContextBuilder()

    context = builder.build([])

    assert context == ""