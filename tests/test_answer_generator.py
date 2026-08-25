import pytest
from app.answer_generator import AnswerGenerator


class FakeLLM:

    def generate(self, prompt: str) -> str:
        return "Employees get 20 days leave."


def test_answer_generator_generates_answer():

    generator = AnswerGenerator(
        llm=FakeLLM(),
    )

    answer = generator.generate(
        query="How many leave days do employees get?",
        context="Employees get 20 days leave.",
    )

    assert answer == "Employees get 20 days leave."


class InspectingLLM:

    def __init__(self):
        self.received_prompt = None

    def generate(self, prompt: str) -> str:
        self.received_prompt = prompt
        return "answer"


def test_answer_generator_includes_query_and_context():

    llm = InspectingLLM()

    generator = AnswerGenerator(llm=llm)

    generator.generate(
        query="How many leave days?",
        context="Employees get 20 days leave.",
    )

    assert "How many leave days?" in llm.received_prompt
    assert "Employees get 20 days leave." in llm.received_prompt


def test_answer_generator_rejects_empty_query():

    generator = AnswerGenerator(
        llm=FakeLLM(),
    )

    with pytest.raises(ValueError, match="query"):
        generator.generate(
            query="",
            context="Employees get 20 days leave.",
        )