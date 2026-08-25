from groq import Groq


def create_groq_client(api_key: str):
    return Groq(api_key=api_key)