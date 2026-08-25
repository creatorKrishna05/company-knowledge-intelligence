import pytest
from app.llm.ollama_llm import OllamaLLM


class FakeOllamaClient:

    def chat(self, model, messages):
        return {
            "message": {
                "content": "The leave policy provides 20 days."
            }
        }


def test_ollama_llm_returns_text():
    client = FakeOllamaClient()

    llm = OllamaLLM(
        client=client,
        model="test-model",
    )

    result = llm.generate("What is the leave policy?")

    assert result == "The leave policy provides 20 days."




class FailingOllamaClient:

    def chat(self, model, messages):
        raise RuntimeError("Ollama server unavailable")


def test_ollama_llm_handles_provider_error():
    client = FailingOllamaClient()

    llm = OllamaLLM(
        client=client,
        model="test-model",
    )

    with pytest.raises(RuntimeError, match="LLM generation failed"):
        llm.generate("Hello")