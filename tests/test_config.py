import pytest

from app.config import Settings


def test_settings_reads_groq_api_key(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-api-key")


    settings = Settings()

    assert settings.groq_api_key == "test-api-key"

def test_settings_requires_groq_api_key(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    with pytest.raises(ValueError, match="GROQ_API_KEY"):
        Settings()


def test_settings_reads_groq_model(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-api-key")
    monkeypatch.setenv("GROQ_MODEL", "test-model")

    settings = Settings()

    assert settings.groq_model == "test-model"