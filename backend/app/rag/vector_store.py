import numpy as np

from app.models.document import DocumentChunk


class VectorStore:

    def __init__(self):
        self.chunks: list[DocumentChunk] = []
        self.embeddings = None

    def add(
        self,
        chunks: list[DocumentChunk],
        embeddings
    ):

        if not chunks:
            return

        embeddings = np.asarray(embeddings)

        self.chunks.extend(chunks)

        if self.embeddings is None:

            self.embeddings = embeddings

        else:

            self.embeddings = np.vstack(
                [
                    self.embeddings,
                    embeddings
                ]
            )

    def search(
        self,
        query_embedding,
        top_k: int = 3
    ):

        if (
            not self.chunks
            or self.embeddings is None
        ):
            return []

        query_embedding = np.asarray(
            query_embedding
        )

        scores = (
            self.embeddings @ query_embedding
        )

        top_k = min(
            top_k,
            len(scores)
        )

        indices = np.argsort(
            scores
        )[::-1][:top_k]

        results = []

        for index in indices:

            results.append(
                {
                    "chunk": self.chunks[index],
                    "score": float(
                        scores[index]
                    )
                }
            )

        return results

    def clear(self):
        self.chunks = []
        self.embeddings = None