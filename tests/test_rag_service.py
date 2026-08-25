import pytest
from app.rag_service import RAGService


class FakeRetriever:

    def __init__(self):
        self.received_filters = None


    def retrieve(self, query, top_k, filters=None):
        self.received_filters = filters
        return ["chunk-1"]


class FakeContextBuilder:

    def build(self, chunks):
        return "Employees get 20 days leave."


class FakeAnswerGenerator:

    def generate(self, query, context):
        return "Employees get 20 days leave."


def test_rag_service_runs_end_to_end():

    service = RAGService(
        retriever=FakeRetriever(),
        context_builder=FakeContextBuilder(),
        answer_generator=FakeAnswerGenerator(),
    )

    answer = service.answer(
        query="How many leave days?",
        top_k=3,
    )

    assert answer == "Employees get 20 days leave."


def test_rag_service_forwards_filters():

    retriever = FakeRetriever()

    service = RAGService(
        retriever=retriever,
        context_builder=FakeContextBuilder(),
        answer_generator=FakeAnswerGenerator(),
    )

    service.answer(
        query="What is leave policy?",
        top_k=3,
        filters={"source": "hr.pdf"},
    )

    assert retriever.received_filters == {"source": "hr.pdf"}


class EmptyRetriever:

    def retrieve(self, query, top_k, filters=None):
        return []


def test_rag_service_returns_controlled_response_when_no_chunks():

    service = RAGService(
        retriever=EmptyRetriever(),
        context_builder=FakeContextBuilder(),
        answer_generator=FakeAnswerGenerator(),
    )

    answer = service.answer(
        query="What is the Mars office policy?",
        top_k=3,
    )

    assert answer == "I couldn't find relevant information in the knowledge base."


class TrackingAnswerGenerator:

    def __init__(self):
        self.called = False

    def generate(self, query, context):
        self.called = True
        return "answer"


def test_rag_service_does_not_generate_when_no_chunks():

    retriever = EmptyRetriever()
    answer_generator = TrackingAnswerGenerator()

    service = RAGService(
        retriever=retriever,
        context_builder=FakeContextBuilder(),
        answer_generator=answer_generator,
    )

    service.answer(
        query="Unknown question",
        top_k=3,
    )

    assert answer_generator.called is False


def test_rag_service_rejects_invalid_top_k():


    service = RAGService(
        retriever=FakeRetriever(),
        context_builder=FakeContextBuilder(),
        answer_generator=FakeAnswerGenerator(),
    )

    with pytest.raises(ValueError, match="top_k"):
        service.answer(
            query="What is the leave policy?",
            top_k=0,
        )