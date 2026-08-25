from app.llm.ollama_client import create_ollama_client


def test_create_ollama_client(monkeypatch):
    fake_client = object()

    monkeypatch.setattr(
        "app.llm.ollama_client.Client",
        lambda **kwargs: fake_client,
    )

    client = create_ollama_client()

    assert client is fake_client