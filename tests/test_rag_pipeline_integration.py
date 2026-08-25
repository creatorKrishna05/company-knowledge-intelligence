from app.answer_generator import AnswerGenerator
from app.context_builder import ContextBuilder
from app.rag_service import RAGService
from app.retrieval_service import RetrievalService
from app.vector_store.in_memory import InMemoryVectorStore
from domain.chunks import Chunk


class FakeEmbedder:

    def embed(self, text: str) -> list[float]:

        if "leave" in text.lower():
            return [1.0, 0.0, 0.0]

        return [0.0, 1.0, 0.0]


class FakeLLM:

    def generate(self, prompt: str) -> str:
        return "Employees get 20 days leave."


def test_rag_pipeline_retrieves_relevant_chunk_and_generates_answer():

    vector_store = InMemoryVectorStore()

    leave_chunk = Chunk(
        "hr.pdf:1:0",
        "Employees get 20 days leave.",
        "hr.pdf",
        1,
        0,
    )

    insurance_chunk = Chunk(
        "hr.pdf:2:0",
        "Company provides health insurance.",
        "hr.pdf",
        2,
        0,
    )

    embedder = FakeEmbedder()

    vector_store.add(
        leave_chunk,
        embedder.embed(leave_chunk.content),
    )

    vector_store.add(
        insurance_chunk,
        embedder.embed(insurance_chunk.content),
    )

    retrieval_service = RetrievalService(
        embedder=embedder,
        vector_store=vector_store,
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
        top_k=1,
    )

    assert answer == "Employees get 20 days leave."