class KnowledgeIngestionService:

    def __init__(
        self,
        ingestion_service,
        cleaner,
        chunker,
        indexing_service,
    ):
        self.ingestion_service = ingestion_service
        self.cleaner = cleaner
        self.chunker = chunker
        self.indexing_service = indexing_service

    def process(self, source: str):
        documents = self.ingestion_service.ingest(source)

        chunks = []

        for document in documents:
            cleaned_document = self.cleaner.clean(document)
            document_chunks = self.chunker.chunk(cleaned_document)
            chunks.extend(document_chunks)

        self.indexing_service.index(chunks)