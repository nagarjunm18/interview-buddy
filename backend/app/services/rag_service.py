from app.rag.chunker import TextChunker
from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore
from app.rag.retriever import Retriever


class RAGService:

    def __init__(self):

        self.chunker = TextChunker()

        self.embedding_service = EmbeddingService()

        self.vector_store = VectorStore()

        self.retriever = Retriever(
            embedding_service=self.embedding_service,
            vector_store=self.vector_store,
            similarity_threshold=0.20
        )

    def index_document(
        self,
        document_id: str,
        text: str,
        metadata: dict | None = None
    ):

        chunks = self.chunker.chunk(
            text=text,
            document_id=document_id,
            metadata=metadata
        )

        if not chunks:
            return 0

        embeddings = self.embedding_service.embed(
            [chunk.text for chunk in chunks]
        )

        self.vector_store.add(
            chunks=chunks,
            embeddings=embeddings
        )

        return len(chunks)

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
        candidate_id: str | None = None
    ):

        results = self.retriever.retrieve(
            query=query,
            top_k=top_k
        )

        if candidate_id is not None:

            results["results"] = [
                result
                for result in results["results"]
                if result["chunk"]
                .metadata
                .get("candidate_id") == candidate_id
            ]

            results["retrieval_success"] = (
                len(results["results"]) > 0
            )

        return results

    def clear(self):
        self.vector_store.clear()