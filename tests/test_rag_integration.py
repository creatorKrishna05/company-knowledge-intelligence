from domain.chunks import Chunk
from app.rag_service import RAGService
from app.retrieval_service import RetrievalService
from app.context_builder import ContextBuilder
from app.answer_generator import AnswerGenerator


class FakeEmbedder:

    def embed(self, text: str) -> list[float]:
        return [1.0, 0.0, 0.0]


class FakeVectorStore:

    def search(
        self,
        query_embedding: list[float],
        top_k: int,
        filters=None,
    ) -> list[Chunk]:

        return [
            Chunk(
                "chunk-1",
                "Employees get 20 days leave.",
                "hr.pdf",
                1,
                0,
            )
        ]


class FakeLLM:

    def generate(self, prompt: str) -> str:
        return "Employees get 20 days leave."


def test_rag_service_end_to_end_with_real_components():

    retrieval_service = RetrievalService(
        embedder=FakeEmbedder(),
        vector_store=FakeVectorStore(),
    )

    context_builder = ContextBuilder()

    answer_generator = AnswerGenerator(
        llm=FakeLLM(),
    )

    rag_service = RAGService(
        retriever=retrieval_service,
        context_builder=context_builder,
        answer_generator=answer_generator,
    )

    answer = rag_service.answer(
        query="How many leave days do employees get?",
        top_k=3,
    )

    assert answer == "Employees get 20 days leave."