import os
import streamlit as st
from ollama import Client

from app.ingestion.registry import LoaderRegistry
from app.ingestion.service import IngestionService
from app.ingestion.loaders.pdf_loader import PDFLoader
from app.cleaning.text_cleaner import TextCleaner
from app.chunking.recursive_chunker import RecursiveChunker
from app.embedding.ollama import OllamaEmbedder
from app.indexing_service import IndexingService
from app.vector_store.in_memory import InMemoryVectorStore
from app.retrieval_service import RetrievalService
from app.context_builder import ContextBuilder
from app.answer_generator import AnswerGenerator
from app.rag_service import RAGService
from app.knowledge_ingestion_service import KnowledgeIngestionService
from app.llm.ollama_client import create_ollama_client
from app.llm.ollama_llm import OllamaLLM


st.set_page_config(
    page_title="Company Knowledge Intelligence",
    page_icon="📚",
)

st.title("📚 Company Knowledge Intelligence")
st.write("Ask questions about company policies and knowledge.")


@st.cache_resource
def create_rag():

    pdf_path = "data/company_knowledge_test.pdf"

    registry = LoaderRegistry()
    registry.register(".pdf", PDFLoader())

    ingestion = IngestionService(registry)
    cleaner = TextCleaner()
    chunker = RecursiveChunker(
        chunk_size=100,
        overlap=20,
    )

    client = Client(
        host=os.getenv("OLLAMA_HOST", "http://localhost:11434")
    )

    embedder = OllamaEmbedder(
        client=client,
        model="nomic-embed-text",
        dimension=768,
    )

    vector_store = InMemoryVectorStore()

    indexer = IndexingService(
        embedder=embedder,
        vector_store=vector_store,
    )

    pipeline = KnowledgeIngestionService(
        ingestion_service=ingestion,
        cleaner=cleaner,
        chunker=chunker,
        indexing_service=indexer,
    )

    pipeline.process(pdf_path)

    retriever = RetrievalService(
        embedder=embedder,
        vector_store=vector_store,
    )

    context_builder = ContextBuilder()

    llm = OllamaLLM(
        client=create_ollama_client(),
        model="llama3.2",
    )

    answer_generator = AnswerGenerator(llm)

    return RAGService(
        retriever=retriever,
        context_builder=context_builder,
        answer_generator=answer_generator,
    )


question = st.text_input(
    "Ask a question",
    placeholder="How many leave days do employees get?",
)


if st.button("Ask"):

    if not question.strip():
        st.warning("Please enter a question.")

    else:
        with st.spinner("Searching company knowledge..."):

            rag = create_rag()

            answer = rag.answer(
                query=question,
                top_k=3,
            )

        st.subheader("Answer")
        st.write(answer)