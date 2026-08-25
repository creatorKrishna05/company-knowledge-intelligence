import pytest

from app.ingestion.service import IngestionService


class FakeLoader:

    def load(self, source):
        self.received_source = source
        return ["fake document"]


class FakeRegistry:

    def __init__(self):
        self.requested_extension = None
        self.loader = FakeLoader()

    def get_loader(self, extension):
        self.requested_extension = extension

        if extension == ".xyz":
            return None

        return self.loader


def test_ingest_and_retrieve_loader():
    registry = FakeRegistry()
    service = IngestionService(registry)

    result = service.ingest("company.pdf")

    assert result == ["fake document"]
    assert registry.requested_extension == ".pdf"


def test_ingest_strips_source_whitespace():
    registry = FakeRegistry()
    service = IngestionService(registry)

    service.ingest("  company.pdf  ")

    assert registry.loader.received_source == "company.pdf"


def test_ingest_rejects_empty_source():
    registry = FakeRegistry()
    service = IngestionService(registry)

    with pytest.raises(ValueError, match="Source cannot be empty"):
        service.ingest("   ")


def test_ingest_rejects_source_without_extension():
    registry = FakeRegistry()
    service = IngestionService(registry)

    with pytest.raises(ValueError, match="Source has no file extension"):
        service.ingest("README")


def test_ingest_rejects_unsupported_extension():
    registry = FakeRegistry()
    service = IngestionService(registry)

    with pytest.raises(ValueError, match="Unsupported file type: .xyz"):
        service.ingest("company.xyz")