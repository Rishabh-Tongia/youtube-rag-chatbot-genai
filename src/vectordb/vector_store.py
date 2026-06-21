import shutil
import os

from langchain_qdrant import QdrantVectorStore


def create_vector_store(
        docs,
        embeddings
):

    if os.path.exists("./qdrant_data"):
        shutil.rmtree("./qdrant_data")

    vector_store = QdrantVectorStore.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name="youtube_rag",
        path="./qdrant_data"
    )

    return vector_store
