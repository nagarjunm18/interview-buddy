from app.services.rag_service import RAGService


def main():

    rag = RAGService()

    resume = """
    Nagarjun M is a Computer Science engineering student.

    He has experience with Java, C++, Python, Spring Boot,
    REST APIs, JWT authentication, MySQL, PostgreSQL,
    MongoDB, AWS, Git and GitHub.

    He built RentMate, a student rental platform using
    Spring Boot, MySQL and JWT authentication.

    He has also worked on AI engineering projects involving
    LLMs, prompt engineering, function calling,
    semantic search and retrieval augmented generation.

    He is interested in backend development, cloud computing
    and AI engineering.
    """

    count = rag.index_document(
        document_id="candidate-resume",
        text=resume,
        metadata={
            "type": "resume"
        }
    )

    print(f"Indexed {count} chunks")

    queries = [
        "What backend technologies does the candidate know?",
        "What project did the candidate build?",
        "What AI engineering concepts does the candidate know?",
        "What is the minimum lease duration for RentMate properties?",
    ]

    for query in queries:

        print("\n" + "=" * 60)
        print("QUERY:", query)

        result = rag.retrieve(
            query=query,
            top_k=3
        )

        print(
            f"Retrieval success: {result['retrieval_success']}"
        )

        print(
            f"Threshold: {result['threshold']}"
        )

        for item in result["results"]:

            print(
                f"\nScore: {item['score']:.4f}"
            )

            print(
                item["chunk"].text
            )


if __name__ == "__main__":
    main()