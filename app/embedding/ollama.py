from app.embedding.base import BaseEmbedder


class OllamaEmbedder(BaseEmbedder):

    def __init__(self, client, model: str, dimension: int):
        self.client = client
        self.model = model
        self._dimension = dimension

    def embed(self, text: str) -> list[float]:
        self._validate_text(text)

        response = self.client.embed(
            model=self.model,
            input=text,
        )

        vector = response["embeddings"][0]

        if len(vector) != self._dimension:
            raise ValueError(
                f"Embedding dimension mismatch: "
                f"expected {self._dimension}, got {len(vector)}"
            )

        return vector

    @property
    def dimension(self) -> int:
        return self._dimension