import pytest
from app.llm.groq_llm import GroqLLM


class FakeMessage:
    content = "Groq generated answer"


class FakeChoice:
    message = FakeMessage()


class FakeResponse:
    choices = [FakeChoice()]


class FakeGroqClient:
    class Chat:
        class Completions:
            @staticmethod
            def create(**kwargs):
                return FakeResponse()

        completions = Completions()

    chat = Chat()


def test_groq_llm_generates_text():
    llm = GroqLLM(
        client=FakeGroqClient(),
        model="fake-model",
    )

    result = llm.generate("What is the leave policy?")


    assert result == "Groq generated answer"


def test_groq_llm_handles_provider_error():

    class FailingGroqClient:
        class Chat:
            class Completions:
                @staticmethod
                def create(**kwargs):
                    raise Exception("Groq API failed")

            completions = Completions()

        chat = Chat()

    llm = GroqLLM(
        client=FailingGroqClient(),
        model="fake-model",
    )

    with pytest.raises(RuntimeError, match="LLM generation failed"):
        llm.generate("What is the leave policy?")