from domain.chunks import Chunk


class ContextBuilder:

    def build(self, chunks: list[Chunk]) -> str:
        if not chunks:
            return ""

        sections = []

        for chunk in chunks:
            section = (
                f"Source: {chunk.source}\n"
                f"Page: {chunk.page}\n"
                f"{chunk.content}"
            )

            sections.append(section)

        return "\n\n".join(sections)