from abc import ABC, abstractmethod
from domain.documents import Document

class BaseCleaner(ABC):

    @abstractmethod
    def clean(self, document: Document) -> Document:
        pass