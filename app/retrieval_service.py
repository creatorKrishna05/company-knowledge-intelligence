from domain.chunks import Chunk
from app.embedding.base import BaseEmbedder
from app.vector_store.base import BaseVectorStore


class RetrievalService:

    def __init__(
        self,
        embedder: BaseEmbedder,
        vector_store: BaseVectorStore,
    ):
        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int,
        filters: dict | None = None,
    ) -> list[Chunk]:

        if not query.strip():
            raise ValueError("query cannot be empty")

        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")

        query_embedding = self.embedder.embed(query)

        return self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            filters=filters,
        )