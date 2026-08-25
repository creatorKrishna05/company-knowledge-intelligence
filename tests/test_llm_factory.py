from app.llm.factory import create_llm


def test_create_groq_llm(monkeypatch):
    fake_client = object()

    monkeypatch.setattr(
        "app.llm.factory.create_groq_client",
        lambda api_key: fake_client,
    )

    llm = create_llm(
        provider="groq",
        api_key="test-api-key",
        model="test-model",
    )

    assert llm.client is fake_client
    assert llm.model == "test-model"


from app.llm.ollama_llm import OllamaLLM


def test_create_ollama_llm(monkeypatch):
    fake_client = object()

    class FakeOllamaLLM:
        def __init__(self, client, model):
            self.client = client
            self.model = model

    monkeypatch.setattr(
        "app.llm.factory.OllamaLLM",
        FakeOllamaLLM,
    )

    llm = create_llm(
        provider="ollama",
        api_key=None,
        model="llama3.2",
    )

    assert llm.client is not None
    assert llm.model == "llama3.2"


from app.llm.ollama_client import create_ollama_client


def test_create_ollama_llm(monkeypatch):
    fake_client = object()

    monkeypatch.setattr(
        "app.llm.factory.create_ollama_client",
        lambda: fake_client,
    )

    llm = create_llm(
        provider="ollama",
        api_key=None,
        model="llama3.2",
    )

    assert llm.client is fake_client
    assert llm.model == "llama3.2"


import pytest


def test_create_llm_rejects_unsupported_provider():
    with pytest.raises(
        ValueError,
        match="Unsupported LLM provider: openai",
    ):
        create_llm(
            provider="openai",
            api_key=None,
            model="test-model",
        )