from pathlib import Path

from ollama import Client

from app.ingestion.registry import LoaderRegistry
from app.ingestion.service import IngestionService
from app.ingestion.loaders.pdf_loader import PDFLoader
from app.cleaning.text_cleaner import TextCleaner
from app.chunking.recursive_chunker import RecursiveChunker
from app.embedding.ollama import OllamaEmbedder
from app.indexing_service import IndexingService
from app.vector_store.in_memory import InMemoryVectorStore
from app.retrieval_service import RetrievalService
from app.knowledge_ingestion_service import KnowledgeIngestionService


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = PROJECT_ROOT / "data" / "company_knowledge_test.pdf"


def test_real_pdf_rag_retrieval():

    # 1. PDF ingestion
    registry = LoaderRegistry()
    registry.register(".pdf", PDFLoader())

    ingestion_service = IngestionService(
        registry=registry,
    )

    # 2. Cleaning + chunking
    cleaner = TextCleaner()

    chunker = RecursiveChunker(
        chunk_size=100,
        overlap=20,
    )

    # 3. Real Ollama embedding
    client = Client()

    embedder = OllamaEmbedder(
        client=client,
        model="nomic-embed-text",
        dimension=768,
    )

    # 4. Real vector store
    vector_store = InMemoryVectorStore()

    indexing_service = IndexingService(
        embedder=embedder,
        vector_store=vector_store,
    )

    # 5. Complete ingestion + indexing
    service = KnowledgeIngestionService(
        ingestion_service=ingestion_service,
        cleaner=cleaner,
        chunker=chunker,
        indexing_service=indexing_service,
    )

    service.process(str(PDF_PATH))

    # 6. Retrieval
    retriever = RetrievalService(
        embedder=embedder,
        vector_store=vector_store,
    )

    results = retriever.retrieve(
        "What is the leave policy?",
        top_k=3,
    )

    assert len(results) > 0
    assert any(
        "leave" in chunk.content.lower()
        for chunk in results
    )