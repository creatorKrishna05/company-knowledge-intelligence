from pypdf import PdfReader


from domain.documents import Document
from app.ingestion.loaders.base import BaseLoader


class PDFLoader(BaseLoader):
    def load(self, source: str) -> list[Document]:
        reader = PdfReader(source)
        documents = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()

            if not text:
                # warning/log
                continue

            documents.append(
                Document(
                    content=text,
                    metadata={
                        "source": str(source),
                        "page": page_number
                    }
                )
                
            )

        return documents

