from pathlib import Path
from domain.documents import Document

class IngestionService:

    def __init__(self, registry):
        self._registry = registry


    def ingest(self, source: str) -> list[Document]:
        source = source.strip()

        if not source:
            raise ValueError("Source cannot be empty")

        extension = Path(source).suffix

        if not extension:
            raise ValueError("Source has no file extension")

        loader = self._registry.get_loader(extension)

        if loader is None:
            raise ValueError(f"Unsupported file type: {extension}")

        return loader.load(source)
        