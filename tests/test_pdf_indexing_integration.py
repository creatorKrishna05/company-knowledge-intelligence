from pathlib import Path

from app.ingestion.registry import LoaderRegistry
from app.ingestion.service import IngestionService
from app.ingestion.loaders.pdf_loader import PDFLoader
from app.cleaning.text_cleaner import TextCleaner
from app.chunking.recursive_chunker import RecursiveChunker
from app.indexing_service import IndexingService
from app.knowledge_ingestion_service import KnowledgeIngestionService


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = PROJECT_ROOT / "data" / "company_knowledge_test.pdf"


class FakeEmbedder:

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [
            [1.0, 0.0, 0.0]
            for _ in texts
        ]


class FakeVectorStore:

    def __init__(self):
        self.items = []

    def add(self, chunk, embedding):
        self.items.append((chunk, embedding))


def test_real_pdf_is_processed_and_indexed():

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

    vector_store = FakeVectorStore()

    indexing_service = IndexingService(
        embedder=FakeEmbedder(),
        vector_store=vector_store,
    )

    service = KnowledgeIngestionService(
        ingestion_service=ingestion_service,
        cleaner=cleaner,
        chunker=chunker,
        indexing_service=indexing_service,
    )

    service.process(str(PDF_PATH))

    assert len(vector_store.items) > 0

    for chunk, embedding in vector_store.items:
        assert chunk.source == str(PDF_PATH)
        assert chunk.page >= 1
        assert chunk.content.strip()
        assert embedding == [1.0, 0.0, 0.0]