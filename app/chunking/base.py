from abc import ABC, abstractmethod
from domain.documents import Document
from domain.chunks import Chunk


class BaseChunker(ABC):

    @abstractmethod
    def chunk(self, document: Document) -> list[Chunk]:
        pass