from app.llm.base import BaseLLM


class GroqLLM(BaseLLM):

    def __init__(self, client, model: str):
        self.client = client
        self.model = model

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
            )

            return response.choices[0].message.content

        except Exception as exc:
            raise RuntimeError("LLM generation failed") from exc