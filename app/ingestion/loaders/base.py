from abc import ABC, abstractmethod

from domain.documents import Document


class BaseLoader(ABC):

    @abstractmethod
    def load(self, source: str) -> list[Document]:
        pass