from langchain_classic.retrievers import EnsembleRetriever

def create_hybrid_retriever(
        bm25_retriever,
        vector_retriever
):

    hybrid = EnsembleRetriever(
        retrievers=[
            bm25_retriever,
            vector_retriever
        ],
        weights=[0.4, 0.6]
    )

    return hybrid