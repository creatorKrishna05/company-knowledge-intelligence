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
from app.context_builder import ContextBuilder
from app.answer_generator import AnswerGenerator
from app.rag_service import RAGService
from app.llm.ollama_client import create_ollama_client
from app.llm.ollama_llm import OllamaLLM
from app.knowledge_ingestion_service import KnowledgeIngestionService


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = PROJECT_ROOT / "data" / "company_knowledge_test.pdf"


def test_end_to_end_rag():

    # Ingestion
    registry = LoaderRegistry()
    registry.register(".pdf", PDFLoader())

    ingestion = IngestionService(registry)

    # Cleaning + Chunking
    cleaner = TextCleaner()
    chunker = RecursiveChunker(
        chunk_size=100,
        overlap=20,
    )

    # Real Ollama embeddings
    client = Client()

    embedder = OllamaEmbedder(
        client=client,
        model="nomic-embed-text",
        dimension=768,
    )

    # Vector store
    vector_store = InMemoryVectorStore()

    indexer = IndexingService(
        embedder=embedder,
        vector_store=vector_store,
    )

    # Complete indexing pipeline
    ingestion_pipeline = KnowledgeIngestionService(
        ingestion_service=ingestion,
        cleaner=cleaner,
        chunker=chunker,
        indexing_service=indexer,
    )

    ingestion_pipeline.process(str(PDF_PATH))

    # Retrieval
    retriever = RetrievalService(
        embedder=embedder,
        vector_store=vector_store,
    )

    # Context
    context_builder = ContextBuilder()

    # Real Ollama LLM
    llm_client = create_ollama_client()

    llm = OllamaLLM(
        client=llm_client,
        model="llama3.2",
    )

    answer_generator = AnswerGenerator(llm)

    # RAG
    rag = RAGService(
        retriever=retriever,
        context_builder=context_builder,
        answer_generator=answer_generator,
    )

    answer = rag.answer(
        query="How many leave days do employees get?",
        top_k=3,
    )

    print("\nANSWER:", answer)

    assert answer
    assert isinstance(answer, str)