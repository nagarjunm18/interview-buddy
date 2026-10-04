from app.models.document import DocumentChunk


class TextChunker:

    def __init__(self, chunk_size: int = 500, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(
        self,
        text: str,
        document_id: str,
        metadata: dict | None = None
    ) -> list[DocumentChunk]:

        text = text.strip()

        if not text:
            return []

        metadata = metadata or {}

        chunks = []
        start = 0
        chunk_number = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    DocumentChunk(
                        chunk_id=f"{document_id}-{chunk_number}",
                        document_id=document_id,
                        text=chunk_text,
                        metadata=metadata
                    )
                )

            if end >= len(text):
                break

            start = end - self.overlap
            chunk_number += 1

        return chunks