from src.loader.youtube_loader import get_transcript
from src.chunking.text_splitter import split_documents
from src.embeddings.embedding_model import get_embedding_model
from src.vectordb.vector_store import create_vector_store
from src.retrieval.retriever import get_retriever
from llm import get_llm
from prompt import get_prompt
from rag_chain import build_chain
from src.utils.time_utils import format_timestamp
from src.reranker.reranker import rerank_documents

url = input("Youtube URL: ")

documents = get_transcript(url)
print("Loading transcript...")

print(f"Loaded {len(documents)} transcript segments")
chunks = split_documents(documents)
print("\nSample Metadata:")
print(chunks[0].metadata)
print(f"Created {len(chunks)} chunks")

embeddings = get_embedding_model()

vector_store = create_vector_store(
    chunks,
    embeddings
)

retriever = get_retriever(
    vector_store
)

llm = get_llm()

prompt = get_prompt()

chain = build_chain(
    retriever,
    prompt,
    llm
)


while True:

    question = input(
        "\nAsk Question: "
    )

    if question.lower() == "exit":
        break

    docs = retriever.invoke(question)

    docs = rerank_documents(
        question,
        docs,
        top_k=3
    )

    print("\nRetrieved Chunks:")
    for doc in docs:
        print(
            doc.metadata["start_time"],
            "-",
            doc.metadata["end_time"]
        )

    response = chain.invoke(question)

    print("\nAnswer:\n")
    print(response)

    print("\nSources:")

    for doc in docs:

        start_time = format_timestamp(
            doc.metadata["start_time"]
        )

        end_time = format_timestamp(
            doc.metadata["end_time"]
        )

        print(
            f"{start_time} - {end_time}"
        )