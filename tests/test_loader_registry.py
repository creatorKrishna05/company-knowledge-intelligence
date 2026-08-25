from app.ingestion.registry import LoaderRegistry
import pytest


def test_register_and_retrieve_loader():
    # Arrange
    registry = LoaderRegistry()
    loader = object()

    # Act
    registry.register(".pdf", loader)
    result = registry.get_loader(".pdf")

    # Assert
    assert result is loader

def test_extension_normalization():
    registry = LoaderRegistry()
    loader = object()

    registry.register(".pdf", loader)
    result = registry.get_loader(".PDF")

    assert result is loader

def test_unknown_extension_returns_none():
    registry = LoaderRegistry()

    result = registry.get_loader(".xyz")

    assert result is None

def test_duplicate_extension_raises_error():
    registry = LoaderRegistry()
    loader_1 = object()
    loader_2 = object()

    registry.register(".pdf", loader_1)

    with pytest.raises(ValueError):
        registry.register(".pdf", loader_2)