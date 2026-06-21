# 🎥 YouTube RAG Chatbot

A Retrieval-Augmented Generation (RAG) based chatbot that allows users to ask questions about YouTube videos using transcript-based semantic search and LLM-generated answers with source grounding.

---

## 🚀 Features

- 🎬 Load any YouTube video via URL
- 🧠 Automatic transcript extraction and chunking
- 🔎 Vector-based semantic search (RAG pipeline)
- 🤖 LLM-powered question answering
- 📌 Source-grounded responses with timestamp references
- 💬 Persistent chat history (Streamlit session memory)
- ⚡ Simple and interactive Streamlit UI

---

## 🏗️ Architecture

### 1. Data Ingestion
- YouTube URL → transcript extraction
- Transcript split into chunks with timestamps

### 2. Embedding Layer
- Text chunks converted into embeddings using embedding model

### 3. Vector Store
- Embeddings stored in vector database (FAISS / Qdrant / similar)

### 4. Retrieval
- User query → embedded → similarity search → top relevant chunks

### 5. Generation
- Retrieved chunks passed to LLM
- LLM generates grounded answer

### 6. UI Layer (Streamlit)
- Input YouTube URL
- Ask questions in chat format
- Displays answers + timestamped sources
- Maintains chat history using session state

---

## 🖥️ Tech Stack

- Python
- Streamlit
- LangChain / Custom RAG pipeline
- Vector Database (FAISS / Qdrant)
- YouTube Transcript API / Loader
- LLM (OpenAI / Groq / similar)
- Embedding Model (sentence-transformers / OpenAI embeddings)

---

## 📂 Project Structure (Simplified)

src/
├── loader/ # YouTube transcript loader
├── chunking/ # Text splitting with timestamps
├── embeddings/ # Embedding model logic
├── vectordb/ # Vector store integration
├── retrieval/ # Retriever logic
├── chatbot.py # RAG pipeline (build + query)
├── utils/
│ └── time_utils.py

streamlit_app.py # UI layer

---

## 💡 How It Works

1. User enters YouTube URL  
2. Transcript is extracted and split into chunks  
3. Chunks are embedded and stored in vector DB  
4. User asks a question  
5. Similar chunks are retrieved using semantic search  
6. LLM generates answer using retrieved context  
7. Sources are shown with video timestamps  

---

## 🧠 Key Features Implemented

- RAG pipeline from scratch
- Timestamp-aware chunking
- Context-based answer generation
- Session-based chat memory
- Streamlit interactive UI
- Source grounding for hallucination control

---

## 📌 Future Improvements

- ChatGPT-style UI (bubbles)
- Clickable timestamp video navigation
- Multi-video memory system
- Reranking (cross-encoder / hybrid search)
- Streaming LLM responses
- Evaluation metrics for RAG quality

---

## ▶️ Run Project

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
