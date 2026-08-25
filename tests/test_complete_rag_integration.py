from pathlib import Path

from app.answer_generator import AnswerGenerator
from app.chunking.recursive_chunker import RecursiveChunker
from app.cleaning.text_cleaner import TextCleaner
from app.ingestion.loaders.pdf_loader import PDFLoader
from app.ingestion.registry import LoaderRegistry
from app.ingestion.service import IngestionService
from app.indexing_service import IndexingService
from app.knowledge_ingestion_service import KnowledgeIngestionService
from app.rag_service import RAGService
from app.retrieval_service import RetrievalService
from app.vector_store.in_memory import InMemoryVectorStore


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = PROJECT_ROOT / "data" / "company_knowledge_test.pdf"


class FakeEmbedder:

    def embed(self, text: str) -> list[float]:
        if "leave" in text.lower():
            return [1.0, 0.0, 0.0]

        return [0.0, 1.0, 0.0]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [self.embed(text) for text in texts]


class FakeLLM:

    def generate(self, prompt: str) -> str:
        return "Employees get 20 days leave."


def test_complete_rag_flow_from_pdf_to_answer():

    registry = LoaderRegistry()
    registry.register(".pdf", PDFLoader())

    ingestion_service = IngestionService(
        registry=registry,
    )

    cleaner = TextCleaner()

    chunker = RecursiveChunker(
        chunk_size=100,
        overlap=20,
    )

    embedder = FakeEmbedder()
    vector_store = InMemoryVectorStore()

    indexing_service = IndexingService(
        embedder=embedder,
        vector_store=vector_store,
    )

    knowledge_ingestion = KnowledgeIngestionService(
        ingestion_service=ingestion_service,
        cleaner=cleaner,
        chunker=chunker,
        indexing_service=indexing_service,
    )

    knowledge_ingestion.process(str(PDF_PATH))

    retrieval_service = RetrievalService(
        embedder=embedder,
        vector_store=vector_store,
    )

    context_builder = __import__(
        "app.context_builder",
        fromlist=["ContextBuilder"],
    ).ContextBuilder()

    answer_generator = AnswerGenerator(
        llm=FakeLLM(),
    )

    rag_service = RAGService(
        retriever=retrieval_service,
        context_builder=context_builder,
        answer_generator=answer_generator,
    )

    answer = rag_service.answer(
        query="How many leave days do employees get?",
        top_k=3,
    )

    assert answer == "Employees get 20 days leave."