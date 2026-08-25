import re
from domain.documents import Document

class TextCleaner:
    def clean(self, document: Document) -> Document:
        content=document.content 

        metadata = document.metadata.copy()

        cleaned_content = content.strip()
        cleaned_content = re.sub(r"[ \t]+", " ", cleaned_content)
        cleaned_content = re.sub("\n{3,}", "\n\n", cleaned_content)
    
        return Document(cleaned_content, metadata)

    