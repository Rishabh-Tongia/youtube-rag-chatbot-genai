from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.documents import Document
import re


def extract_video_id(url):

    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})"

    match = re.search(pattern, url)

    if match:
        return match.group(1)

    raise ValueError("Invalid YouTube URL")


def get_transcript(url):

    video_id = extract_video_id(url)

    ytt_api = YouTubeTranscriptApi()

    transcript = ytt_api.fetch(
        video_id,
        languages=["en", "hi"]
    )

    documents = []

    window_size = 20

    for i in range(0, len(transcript), window_size):

        window = transcript[i:i + window_size]

        text = " ".join(
            snippet.text
            for snippet in window
        )

        start_time = window[0].start

        end_time = (
            window[-1].start
            + window[-1].duration
        )

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "video_id": video_id,
                    "start_time": start_time,
                    "end_time": end_time
                }
            )
        )

    return documents