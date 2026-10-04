from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore


class Retriever:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        similarity_threshold: float = 0.20
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.similarity_threshold = similarity_threshold

    def retrieve(
        self,
        query: str,
        top_k: int = 3
    ):
        query_embedding = self.embedding_service.embed(
            [query]
        )[0]

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k
        )

        relevant_results = [
            result
            for result in results
            if result["score"] >= self.similarity_threshold
        ]

        return {
            "query": query,
            "results": relevant_results,
            "retrieval_success": len(relevant_results) > 0,
            "threshold": self.similarity_threshold
        }