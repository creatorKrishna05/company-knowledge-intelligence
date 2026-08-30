import os

from huggingface_hub import InferenceClient

from app.embedding.base import BaseEmbedder


class HuggingFaceEmbedder(BaseEmbedder):

    def __init__(
        self,
        client: InferenceClient,
        model: str,
        dimension: int,
    ):
        self.client = client
        self.model = model
        self._dimension = dimension

    def embed(self, text: str) -> list[float]:
        self._validate_text(text)

        response = self.client.feature_extraction(
            text,
            model=self.model,
        )

        vector = response.tolist()

        if len(vector) != self._dimension:
            raise ValueError(
                f"Embedding dimension mismatch: "
                f"expected {self._dimension}, got {len(vector)}"
            )

        return vector

    @property
    def dimension(self) -> int:
        return self._dimension