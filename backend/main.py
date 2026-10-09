from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.chatbot import build_rag_system, ask_question

class VideoRequest(BaseModel):
    url: str

class QuestionRequest(BaseModel):
    question: str

class Source(BaseModel):
    start_time: float
    end_time: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_system = None

@app.get("/")
def root():
    return {"message": "YouTube RAG Chatbot API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/api/load-video")
def load_video(request: VideoRequest):
    global rag_system

    if "youtube.com" not in request.url and "youtu.be" not in request.url:
        raise HTTPException(
            status_code=400,
            detail="Please provide a valid YouTube URL."
        )

    try:
        rag_system = build_rag_system(request.url)

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to load video: {str(e)}"
        )

    return {
        "message": "Video loaded successfully"
    }

@app.post("/api/chat", response_model=ChatResponse)
def chat(request: QuestionRequest):

    if rag_system is None:
        raise HTTPException(
            status_code=400,
            detail="Please load a video before asking a question."
        )

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    answer, docs = ask_question(
        request.question,
        rag_system
    )

    sources = []

    for doc in docs:
        sources.append({
            "start_time": doc.metadata.get("start_time", 0),
            "end_time": doc.metadata.get("end_time", 0)
        })

    return {
        "answer": answer,
        "sources": sources
    }