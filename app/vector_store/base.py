from abc import ABC, abstractmethod

from domain.chunks import Chunk

class BaseVectorStore(ABC):

    @abstractmethod
    def add (self, chunk:Chunk, embedding: list[float]) -> None:
        ...

    @abstractmethod
    def search(
        self,
        query_embedding: list[float],
        top_k: int,
        filters: dict | None = None,
    ) -> list[Chunk]:
        ...