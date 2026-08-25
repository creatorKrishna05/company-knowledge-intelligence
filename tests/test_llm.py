from app.llm.base import BaseLLM


def test_llm_requires_implementation():

    class FakeLLM(BaseLLM):

        def generate(self, prompt: str) -> str:
            return "fake answer"

    llm = FakeLLM()

    assert llm.generate("Hello") == "fake answer"