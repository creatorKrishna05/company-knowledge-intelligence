from dataclasses import dataclass

@dataclass
class Chunk:
    chunk_id: str
    content: str
    source: str
    page: int
    chunk_index: int 