from domain.documents import Document
from app.cleaning.text_cleaner import TextCleaner

def test_whitespace_normalization():
    document = Document(
    content="Company   Policy\t\tLeave",
    metadata={"source": "test"}
    )
    cleaner = TextCleaner()
    cleaned_document = cleaner.clean(document)

    assert cleaned_document.content == "Company Policy Leave"

def test_excessive_blank_lines():
    document = Document(
        content="Company Policy\n\n\n\nLeave Policy",
        metadata={"source": "test"}
    )
    cleaner = TextCleaner()
    cleaned_document = cleaner.clean(document)

    assert cleaned_document.content == "Company Policy\n\nLeave Policy"

def test_leading_and_trailing_whitespace():
    document = Document(
        content="   Company Policy  Leave Policy  ",
        metadata={"source": "test"}
    )
    cleaner  = TextCleaner()
    cleaned_document = cleaner.clean(document)

    assert cleaned_document.content == "Company Policy Leave Policy"


def test_metadata_preserved():
    document = Document(
        content="  Company Policy  ",
        metadata={"source": "policy.pdf", "page": 4}
    )

    cleaner = TextCleaner()
    cleaned_document = cleaner.clean(document)

    assert cleaned_document.metadata == {"source": "policy.pdf", "page": 4}