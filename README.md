# 🎥 YouTube RAG Chatbot

A Retrieval-Augmented Generation (RAG) application that lets users ask natural-language questions about YouTube videos. It retrieves relevant transcript segments using hybrid search, reranks the results, and generates context-grounded answers using Google's Gemini 2.5 Flash.

The project combines a **React frontend** with a **FastAPI backend** and a retrieval pipeline built with Python, LangChain, and Qdrant.

---

## 🚀 Features

- 🎬 Load a YouTube video using its URL
- 📝 Extract video transcripts and split them into timestamp-aware chunks
- 🧠 Generate embeddings for semantic retrieval
- 🗄️ Store and retrieve transcript embeddings using Qdrant
- 🔎 Combine BM25 keyword retrieval with semantic vector search
- 🎯 Rerank retrieved transcript segments before answer generation
- 🤖 Generate context-grounded answers using Gemini 2.5 Flash
- 📌 Display source transcript segments with their start and end timestamps
- ⚛️ Interactive React frontend
- ⚡ FastAPI REST endpoints for video loading and question answering

---

## 🏗️ Architecture

The application follows a frontend-backend architecture, with the RAG pipeline handling retrieval and answer generation.

### High-Level Workflow

```text
                  User
                   |
                   v
             React Frontend
                   |
             HTTP REST APIs
                   |
                   v
             FastAPI Backend
                   |
           YouTube Transcript
                   |
                   v
             Text Chunking
                   |
                   v
                Embeddings
                   |
                   v
             Qdrant Vector Store
                   |
          +--------+--------+
          |                 |
          v                 v
    Semantic Search     BM25 Search
          |                 |
          +--------+--------+
                   |
                   v
            Hybrid Retrieval
                   |
                   v
             Document Reranking
                   |
                   v
          Context + User Question
                   |
                   v
            Gemini 2.5 Flash
                   |
                   v
       Answer + Source Timestamps
                   |
                   v
             React Frontend
```

### 1. Video Ingestion

- The user submits a YouTube video URL through the React interface.
- The backend extracts the available transcript.
- The transcript is divided into smaller chunks while preserving relevant metadata, including timestamps.

### 2. Embedding Generation

- An embedding model converts transcript chunks into numerical vector representations.
- These vectors allow semantically related text to be retrieved even when the wording differs from the user's question.

### 3. Vector Storage

- Qdrant stores the transcript embeddings and associated document information.
- The vector retriever searches for transcript chunks relevant to the user's question.

### 4. Hybrid Retrieval

The application combines two retrieval approaches:

- **Semantic vector search:** Retrieves chunks based on the meaning of the query.
- **BM25 keyword search:** Retrieves chunks based on keyword relevance.

The hybrid retriever combines these approaches to obtain relevant transcript segments for the next stage.

### 5. Document Reranking

- The retrieved documents are reranked for relevance to the user's question.
- The pipeline selects the top three documents for answer generation.

### 6. Answer Generation

- The selected transcript chunks are combined into a context.
- A prompt instructs Gemini 2.5 Flash to answer using the supplied context.
- If the available context does not contain the answer, the model is instructed to acknowledge that limitation.

### 7. Frontend and Backend Integration

- **React:** Provides the interface for entering video URLs, asking questions, and viewing answers and sources.
- **FastAPI:** Exposes REST endpoints for loading videos and answering questions.
- **Pydantic:** Defines and validates request and response data models.
- **CORS middleware:** Allows the local React development server to communicate with the FastAPI backend.

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Language | Python, JavaScript |
| Frontend | React, Vite, HTML, CSS |
| Backend | FastAPI, Uvicorn |
| LLM | Google Gemini 2.5 Flash |
| RAG Framework | LangChain |
| Vector Database | Qdrant |
| Retrieval | BM25, semantic vector search, hybrid retrieval |
| Reranking | Document reranking |
| Embeddings | Hugging Face embedding model |
| Data Source | YouTube video transcripts |
| API Testing | Postman |
| Version Control | Git, GitHub |

---

## 📂 Project Structure

The following is a simplified view of the main application files.

```text
youtube-rag-chatbot/
│
├── backend/
│   └── main.py                  # FastAPI application and REST endpoints
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx               # Main React interface and API calls
│   │   ├── App.css               # Application styles
│   │   ├── index.css             # Global styles
│   │   └── main.jsx              # React entry point
│   ├── index.html
│   └── package.json
│
├── src/
│   ├── loader/
│   │   └── youtube_loader.py     # Transcript extraction
│   ├── chunking/
│   │   └── text_splitter.py      # Transcript chunking
│   ├── embeddings/
│   │   └── embedding_model.py    # Embedding model initialization
│   ├── vectordb/
│   │   └── vector_store.py       # Qdrant vector store
│   ├── retrieval/
│   │   ├── retriever.py          # Semantic retrieval
│   │   ├── bm25_retriever.py     # BM25 keyword retrieval
│   │   └── hybrid_retriever.py   # Hybrid retrieval
│   ├── reranker/
│   │   └── reranker.py           # Document reranking
│   └── chatbot.py                # RAG pipeline orchestration
│
├── llm.py                        # Gemini model configuration
├── prompt.py                     # Answer-generation prompt
├── streamlit_app.py              # Original Streamlit interface
├── app.py                        # Existing CLI entry point
├── requirements.txt              # Python dependencies
└── README.md
```

*Note: This is a simplified structure. Some files and supporting modules may be omitted.*

---

## ⚙️ Setup and Installation

### Prerequisites

- Python installed
- Node.js and npm installed
- A Google Gemini API key
- Git, if cloning the repository

### 1. Clone the Repository

```bash
git clone https://github.com/Rishabh-Tongia/youtube-rag-chatbot-genai.git
cd youtube-rag-chatbot-genai
```

### 2. Create a Python Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API Key

Set the API key according to the environment variable name used in `llm.py`. For example, if the code reads `GOOGLE_API_KEY`, run:

```powershell
$env:GOOGLE_API_KEY="your_api_key_here"
```

Use the exact variable name expected by your implementation. Do not commit API keys or other secrets to GitHub.

### 5. Start the FastAPI Backend

From the project root, run:

```bash
python -m uvicorn backend.main:app --reload
```

The backend should be available at:

- API base: `http://127.0.0.1:8000`
- Interactive API documentation: `http://127.0.0.1:8000/docs`
- Health endpoint: `http://127.0.0.1:8000/health`

### 6. Start the React Frontend

Open a **second terminal** and navigate to the frontend directory:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite, typically:

`http://localhost:5173`

---

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Check the API welcome response |
| `GET` | `/health` | Check backend health |
| `POST` | `/api/load-video` | Extract a transcript and build the RAG system |
| `POST` | `/api/chat` | Answer a question about the loaded video |

### Load a Video

**Request**

```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Example response**

```json
{
  "message": "Video loaded successfully"
}
```

### Ask a Question

**Request**

```json
{
  "question": "What are the main topics discussed in this video?"
}
```

**Example response shape**

```json
{
  "answer": "The video discusses the main topics found in the retrieved transcript context.",
  "sources": [
    {
      "start_time": 65.0,
      "end_time": 92.0
    }
  ]
}
```

*The answer and timestamps above are illustrative. Actual responses depend on the video and retrieved transcript segments.*

---

## 💡 How to Use

1. Start the FastAPI backend and React frontend.
2. Open the application in your browser.
3. Enter a YouTube video URL and select **Load Video**.
4. Wait for the video transcript and retrieval system to finish loading.
5. Enter a question about the video and select **Ask**.
6. Read the generated answer and inspect the associated source timestamps.

---

## 🧠 Key Technical Concepts Demonstrated

- Retrieval-Augmented Generation (RAG)
- Transcript ingestion and text chunking
- Embedding-based semantic retrieval
- Qdrant vector storage
- BM25 keyword retrieval
- Hybrid retrieval and document reranking
- Context-grounded LLM generation
- REST API development with FastAPI
- Frontend-backend integration with React
- Request validation and HTTP error handling

---

## ⚠️ Current Limitations

- Answers depend on the availability and quality of the video's transcript.
- Retrieval quality depends on chunking, embeddings, and the relevance of retrieved documents.
- The current backend keeps the active RAG system in process memory and is designed for a local demonstration rather than concurrent multi-user production use.
- Loading a new video rebuilds the current retrieval system, which can take time.
- The application does not currently provide persistent, cross-session chat history in the React interface.
- Source timestamps identify relevant transcript segments; they are not a guarantee that every answer is fully supported by the retrieved context.

---

## 🔮 Possible Future Improvements

- Persistent conversation history
- Multi-video retrieval and management
- Streaming answer generation
- Automated RAG evaluation using retrieval and answer-quality metrics
- More robust video URL validation and session management
- Production deployment with authentication and monitoring

---

## 📜 License

Add a license if you intend to distribute the project for reuse. Until a license is added, the repository should not be assumed to grant permission for unrestricted reuse.
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
