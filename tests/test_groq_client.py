from app.llm.groq_client import create_groq_client

def test_create_groq_client(monkeypatch):
    monkeypatch.setattr(
        "app.llm.groq_client.Groq",
        lambda api_key: api_key,
    )

    client = create_groq_client("test-api-key")

    assert client == "test-api-key"