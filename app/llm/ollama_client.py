import os

from ollama import Client


def create_ollama_client():
    return Client(
        host=os.getenv("OLLAMA_HOST", "http://localhost:11434")
    )