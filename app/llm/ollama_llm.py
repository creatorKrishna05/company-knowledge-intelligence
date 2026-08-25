from app.llm.base import BaseLLM


class OllamaLLM(BaseLLM):

    def __init__(self, client, model: str):
        self.client = client
        self.model = model

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
            )

            return response["message"]["content"]

        except Exception as exc:
            raise RuntimeError("LLM generation failed") from exc