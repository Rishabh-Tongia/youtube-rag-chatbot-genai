import { useState } from 'react'
import './App.css'

function App() {
  const [videoUrl, setVideoUrl] = useState('')
  const [status, setStatus] = useState('')
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [sources, setSources] = useState([])

  async function handleLoadVideo() {
    if (!videoUrl.trim()) {
      setStatus('Please enter a YouTube URL.')
      return
    }

    try {
      setStatus('Loading video... Please wait.')
      const response = await fetch(
        'http://127.0.0.1:8000/api/load-video',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ url: videoUrl }),
        }
      )

      const data = await response.json()

      if (!response.ok) {
        setStatus(data.detail || 'Failed to load video.')
        return
      }

      setStatus(data.message)
    } catch {
      setStatus('Could not connect to the backend. Check that FastAPI is running.')
    }
  }


  async function handleAskQuestion() {
    if (!question.trim()) {
      setAnswer('Please enter a question.')
      return
    }

    try {
      const response = await fetch(
        'http://127.0.0.1:8000/api/chat',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ question: question }),
        }
      )

      const data = await response.json()

      if (!response.ok) {
        setAnswer(data.detail || 'Failed to get an answer.')
        return
      }

      setAnswer(data.answer)
      setSources(data.sources)
    } catch {
      alert('Could not connect to the backend. Check that FastAPI is running.')
    }
  }


  function formatTime(seconds) {
    const totalSeconds = Math.floor(seconds)
    const minutes = Math.floor(totalSeconds / 60)
    const remainingSeconds = totalSeconds % 60

    return `${minutes}:${String(remainingSeconds).padStart(2, '0')}`
  }

  return (
    <div className='app-container'>
      <h1>YouTube RAG Chatbot</h1>
      <p className="subtitle">Load a YouTube video and ask questions about its content.</p>

      <div className="video-form">
        <input
          type="text"
          placeholder="Paste YouTube URL here"
          value={videoUrl}
          onChange={(event) => setVideoUrl(event.target.value)}
        />

        <button type="button" onClick={handleLoadVideo}>
          Load Video
        </button>
      </div>
      <p
        role="status"
        className={
          status.includes('successfully')
            ? 'status-message success'
            : status.startsWith('Loading')
              ? 'status-message loading'
              : status
                ? 'status-message error'
                : ''
        }
      >
        {status}
      </p>

      <div className="chat-section">
        <h2>Ask Questions</h2>

        <div className="question-form">
          <input
            type="text"
            placeholder="Ask something about the video..."
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
          />

          <button type="button" onClick={handleAskQuestion}>
            Ask
          </button>
        </div>
      </div>

      {answer && (
        <div className="answer-box">
          <h3>Answer</h3>
          <p>{answer}</p>

          {sources.length > 0 && (
            <div className="sources-section">
              <h4>Sources from the video</h4>

              {sources.map((source, index) => (
                <p key={index} className="source-item">
                  Source {index + 1}: {formatTime(source.start_time)} –{' '}
                  {formatTime(source.end_time)}
                </p>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default App