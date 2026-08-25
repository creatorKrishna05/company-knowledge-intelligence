import math 
from domain.chunks import Chunk
from app.vector_store.base import BaseVectorStore

class InMemoryVectorStore(BaseVectorStore):

    def __init__(self):
        self._items: list[tuple[Chunk, list[float]]] = []

    def add(self, chunk: Chunk, embedding: list[float]) -> None:
        self._items.append((chunk, embedding))

    def search(
        self,
        query_embedding: list[float],
        top_k: int,
        filters: dict | None = None,
    ) -> list[Chunk]:

        scored = []

        for chunk, embedding in self._items:

            if filters:
                if "source" in filters and chunk.source != filters["source"]:
                    continue

                
            score = self._cosine_similarity(query_embedding, embedding)
            scored.append((score, chunk))

        scored.sort(key=lambda item: item[0], reverse=True)

        return [chunk for score, chunk in scored[:top_k]]

    def _cosine_similarity(
        self,
        a: list[float],
        b: list[float],
    ) -> float:
        dot = sum(x * y for x, y in zip(a, b))

        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot / (norm_a * norm_b)