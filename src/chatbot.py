from src.loader.youtube_loader import get_transcript
from src.chunking.text_splitter import split_documents
from src.embeddings.embedding_model import get_embedding_model
from src.vectordb.vector_store import create_vector_store

from src.retrieval.retriever import get_retriever
from src.retrieval.bm25_retriever import create_bm25_retriever
from src.retrieval.hybrid_retriever import create_hybrid_retriever

from src.reranker.reranker import rerank_documents

from llm import get_llm
from prompt import get_prompt

def build_rag_system(url):

    documents = get_transcript(url)

    chunks = split_documents(documents)

    embeddings = get_embedding_model()

    vector_store = create_vector_store(
        chunks,
        embeddings
    )

    vector_retriever = get_retriever(
        vector_store
    )

    bm25_retriever = create_bm25_retriever(
        chunks
    )

    hybrid_retriever = create_hybrid_retriever(
        bm25_retriever,
        vector_retriever
    )

    llm = get_llm()

    return {
        "retriever": hybrid_retriever,
        "llm": llm
    }




def ask_question(question, rag_system):

    retriever = rag_system["retriever"]

    docs = retriever.invoke(question)

    docs = rerank_documents(
        question,
        docs,
        top_k=3
    )

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = get_prompt()

    messages = prompt.invoke({
        "context": context,
        "question": question
    })

    llm = rag_system["llm"]

    answer = llm.invoke(messages)

    return answer.content, docs