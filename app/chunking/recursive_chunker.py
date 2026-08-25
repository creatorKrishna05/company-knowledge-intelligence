from domain.documents import Document
from domain.chunks import Chunk
from app.chunking.base import BaseChunker


class RecursiveChunker(BaseChunker):

    def __init__(self, chunk_size: int, overlap: int):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0")

        if overlap < 0:
            raise ValueError("overlap cannot be negative")

        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.overlap = overlap

    def _split_text(self, text: str, separator: str) -> list[str]:
        return text.split(separator)

    def chunk(self, document: Document) -> list[Chunk]:
        content = document.content
        separators = ["\n\n", "\n", " ", ""]
        pieces = self._recursive_split(content, separators)
        pieces = self._apply_overlap(pieces)

        source = document.metadata["source"]
        page = document.metadata["page"]

        chunks = []
        chunk_index = 0

        for piece in pieces:
            chunk_id = f"{source}:{page}:{chunk_index}"

            chunk = Chunk(
                chunk_id=chunk_id,
                content=piece,
                source=source,
                page=page,
                chunk_index=chunk_index,
            )

            chunks.append(chunk)
            chunk_index += 1

        return chunks

    def _recursive_split(
        self,
        text: str,
        separators: list[str],
    ) -> list[str]:

        if not separators:
            return [text]

        separator = separators[0]

        if separator == "":
            return[
                text[i:i + self.chunk_size]
                for i in range(0, len(text), self.chunk_size)
            ]
        pieces = self._split_text(text, separator)

        result = []

        for piece in pieces:
            if len(piece) <= self.chunk_size:
                result.append(piece)
            else:
                result.extend(
                    self._recursive_split(piece, separators[1:])
                )

        return result

    def _apply_overlap(self, pieces: list[str]) -> list[str]:
        if self.overlap == 0:
            return pieces

        result = [pieces[0]]

        for piece in pieces[1:]:
            previous = result[-1]
            overlap_text = previous[-self.overlap:]

            result.append(overlap_text + piece)

        return result

       