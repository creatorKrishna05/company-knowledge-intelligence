import pytest
from app.embedding.ollama import OllamaEmbedder
from app.vector_store.in_memory import InMemoryVectorStore
from app.retrieval_service import RetrievalService
from domain.chunks import Chunk
from ollama import Client


@pytest.mark.ollama
def test_real_ollama_retrieval():

    client = Client()

    embedder = OllamaEmbedder(
        client=client,
        model="nomic-embed-text",
        dimension=768,
    )

    vector_store = InMemoryVectorStore()

    chunk = Chunk(
        "hr:1:0",
        "Employees receive 20 days of annual leave.",
        "hr.pdf",
        1,
        0,
    )

    embedding = embedder.embed(chunk.content)

    vector_store.add(
        chunk,
        embedding,
    )

    retriever = RetrievalService(
        embedder=embedder,
        vector_store=vector_store,
    )

    results = retriever.retrieve(
        "How many annual leave days do employees receive?",
        top_k=1,
    )

    assert len(results) == 1
    assert results[0].content == chunk.content