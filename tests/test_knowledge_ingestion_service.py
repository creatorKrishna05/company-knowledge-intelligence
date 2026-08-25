from domain.documents import Document
from domain.chunks import Chunk
from app.knowledge_ingestion_service import KnowledgeIngestionService


class FakeIngestionService:

    def ingest(self, source: str) -> list[Document]:
        return [
            Document(
                "  Employees   get 20 days leave.  ",
                {
                    "source": "hr.pdf",
                    "page": 1,
                },
            )
        ]


class FakeCleaner:

    def clean(self, document: Document) -> Document:
        return Document(
            document.content.strip(),
            document.metadata.copy(),
        )


class FakeChunker:

    def chunk(self, document: Document) -> list[Chunk]:
        return [
            Chunk(
                "hr.pdf:1:0",
                document.content,
                "hr.pdf",
                1,
                0,
            )
        ]


class FakeIndexer:

    def __init__(self):
        self.received_chunks = None

    def index(self, chunks):
        self.received_chunks = chunks


def test_knowledge_ingestion_processes_and_indexes_document():

    ingestion = FakeIngestionService()
    cleaner = FakeCleaner()
    chunker = FakeChunker()
    indexer = FakeIndexer()

    service = KnowledgeIngestionService(
        ingestion_service=ingestion,
        cleaner=cleaner,
        chunker=chunker,
        indexing_service=indexer,
    )

    service.process("hr.pdf")

    assert indexer.received_chunks is not None
    assert len(indexer.received_chunks) == 1
    assert indexer.received_chunks[0].content == "Employees   get 20 days leave."