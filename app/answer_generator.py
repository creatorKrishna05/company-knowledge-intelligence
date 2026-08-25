from app.llm.base import BaseLLM


class AnswerGenerator:

    def __init__(self, llm: BaseLLM):
        self.llm = llm

    def generate(self, query: str, context: str) -> str:
        if not query.strip():
            raise ValueError("query cannot be empty")

        if not context.strip():
            raise ValueError("context cannot be empty")

        prompt = f"""
Answer the question using ONLY the provided context.

If the answer is not present in the context, say:
"I couldn't find this information in the knowledge base."

Always include the source and page number from the context when answering.


Context:
{context}

Question:
{query}

Answer:
""".strip()

        return self.llm.generate(prompt)