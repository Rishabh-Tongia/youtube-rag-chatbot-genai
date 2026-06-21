def get_retriever(vector_store):

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 10
        }
    )

    return retriever