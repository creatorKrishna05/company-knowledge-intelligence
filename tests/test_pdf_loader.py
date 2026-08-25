from pathlib import Path
from unittest.mock import patch
from app.ingestion.loaders.pdf_loader import PDFLoader

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PDF_PATH = PROJECT_ROOT / "data" / "company_knowledge_test.pdf"

def test_pdf_loader():
    loader = PDFLoader()
    documents = loader.load(PDF_PATH)

    assert len(documents) == 3

    assert documents[0].metadata["source"] == str(PDF_PATH)
    assert documents[0].metadata["page"] == 1
    
    assert "Company Overview" in documents[0].content
    assert "Leave Policy" in documents[1].content
    assert "Security Policy" in documents[2].content


class FakePage:
    def __init__(self, text):
        self.text = text

    def extract_text(self):
        return self.text

class FakeReader:
    def __init__(self, pages):
        self.pages = pages

def test_pdf_loader_skips_empty_pages():
        fake_reader = FakeReader([
            FakePage("Page one"),
            FakePage(None),
            FakePage("Page three")
        ])

        with patch("app.ingestion.loaders.pdf_loader.PdfReader") as mock_reader:
            mock_reader.return_value = fake_reader

            loader = PDFLoader()
            documents = loader.load(PDF_PATH)

            assert len(documents) == 2
            assert "Page one" in documents[0].content
            assert "Page three" in documents[1].content


       