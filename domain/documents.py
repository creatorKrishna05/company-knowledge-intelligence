from dataclasses import dataclass
from typing import Any


@dataclass
class Document:
    content: str
    metadata: dict[str, Any]