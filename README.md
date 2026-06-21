# YouTube RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that allows users to ask questions about YouTube videos and receive grounded answers with timestamp citations.

## Features

- YouTube Transcript Ingestion
- Semantic Search using Qdrant
- BM25 Retrieval
- Hybrid Search
- Cross Encoder Reranking
- Timestamp Grounding
- Source Attribution

## Tech Stack

- Python
- LangChain
- HuggingFace
- Qdrant
- BM25
- Cross Encoder
- YouTube Transcript API

## Architecture

YouTube Transcript
    ↓
Chunking
    ↓
Embeddings
    ↓
Qdrant + BM25
    ↓
Hybrid Retrieval
    ↓
Cross Encoder Reranking
    ↓
LLM
    ↓
Answer + Timestamps

## Future Improvements

- Streamlit UI
- Conversational Memory
- Multi-Video Support
- RAGAS Evaluation
- Multimodal RAG (PDF, DOCX, PPTX)