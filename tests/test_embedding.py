import pytest
from app.embedding.base import BaseEmbedder
from app.embedding.ollama import OllamaEmbedder


class FakeEmbedder(BaseEmbedder):

    @property
    def dimension(self) -> int:
        return 3

    def embed(self, text: str) -> list[float]:
        self._validate_text(text)
        return [0.1, 0.2, 0.3]


def test_embed_returns_vector():
    embedder = FakeEmbedder()

    vector = embedder.embed("Company leave policy")

    assert isinstance(vector, list)
    assert len(vector) > 0


def test_embed_batch_returns_vectors():
    embedder = FakeEmbedder()

    vectors = embedder.embed_batch([
        "Company leave policy",
        "Work from home policy",
    ])

    assert len(vectors) == 2
    assert all(isinstance(vector, list) for vector in vectors)


def test_embed_rejects_whitespace_only_text():
    embedder = FakeEmbedder()

    with pytest.raises(ValueError):
        embedder.embed("   ")


def test_embed_batch_rejects_empty_text():
    embedder = FakeEmbedder()

    with pytest.raises(ValueError):
        embedder.embed_batch([
            "Company leave policy",
            " ",
        ])


def test_embed_rejects_non_string_text():
    embedder = FakeEmbedder()

    with pytest.raises(TypeError):
        embedder.embed(123)


def test_embedder_exposes_dimension():
    embedder = FakeEmbedder()

    assert embedder.dimension == 3


def test_ollama_embedder_returns_embedding():
    client = FakeOllama()

    embedder = OllamaEmbedder(
        client,
        model="nomic-embed-text",
        dimension=3,
    )

    vector = embedder.embed("Company leave policy")

    assert vector == [0.1, 0.2, 0.3]


def test_ollama_embedder_passes_model_and_input():
    client = FakeOllama()

    embedder = OllamaEmbedder(
        client,
        model="nomic-embed-text",
        dimension=3
    )

    embedder.embed("Company leave policy")

    assert client.model == "nomic-embed-text"
    assert client.input == "Company leave policy"


class FakeOllama:

    def embed(self, model, input):
        self.model = model
        self.input = input

        return {
            "embeddings": [[0.1, 0.2, 0.3]]
        }


def test_ollama_embedder_exposes_dimension():
    client = FakeOllama()

    embedder = OllamaEmbedder(
        client,
        model="nomic-embed-text",
        dimension=3,
    )


def test_ollama_embedder_rejects_wrong_dimension():
    client = FakeOllama()

    embedder = OllamaEmbedder(
        client,
        model="nomic-embed-text",
        dimension=768,
    )

    with pytest.raises(ValueError):
        embedder.embed("Company leave policy")