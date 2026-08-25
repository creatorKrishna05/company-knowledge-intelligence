from app.llm.groq_client import create_groq_client
from app.llm.groq_llm import GroqLLM
from app.llm.ollama_client import create_ollama_client
from app.llm.ollama_llm import OllamaLLM


def create_llm(provider: str, api_key: str, model: str):

    if provider == "groq":
        client = create_groq_client(api_key)

        return GroqLLM(
            client=client,
            model=model,
        )

    if provider == "ollama":
        client = create_ollama_client()

        return OllamaLLM(
            client=client,
            model=model,
        )

    raise ValueError(f"Unsupported LLM provider: {provider}")