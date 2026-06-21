import streamlit as st
from src.utils.time_utils import format_timestamp
from src.chatbot import build_rag_system, ask_question

st.set_page_config(
    page_title="YouTube RAG Chatbot",
    page_icon="",
    layout="centered"
)

st.title(" YouTube RAG Chatbot")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "video_loaded" not in st.session_state:
    st.session_state.video_loaded = False

if "rag_system" not in st.session_state:
    st.session_state.rag_system = None

url = st.text_input("YouTube URL")

if st.button("Load Video"):
    if not url:
        st.error(" Please enter a valid YouTube URL")
    else:
        with st.spinner("Processing Video..."):
            rag_system = build_rag_system(url)

            st.session_state.rag_system = rag_system
            st.session_state.video_loaded = True
            st.session_state.chat_history = []  # reset chat per video

        st.success(" Video Loaded Successfully!")
        st.info(f"Loaded URL: {url}")


if st.session_state.video_loaded and st.session_state.rag_system:

    st.markdown("---")
    st.subheader(" Chat with the Video")


    for chat in st.session_state.chat_history:
        st.markdown(f"You: {chat['q']}")
        st.markdown(f"Bot: {chat['a']}")

        if chat.get("docs"):
            st.markdown("Sources:")
            for doc in chat["docs"]:
                start_time = format_timestamp(doc.metadata.get("start_time", 0))
                end_time = format_timestamp(doc.metadata.get("end_time", 0))
                st.markdown(f"- `{start_time} → {end_time}`")

        st.markdown("---")

    question = st.text_input("Your Question", key="question_input")

    if st.button("Ask Question"):
        if not question:
            st.warning(" Please enter a question")
        else:
            with st.spinner("Generating Answer..."):
                answer, docs = ask_question(
                    question,
                    st.session_state.rag_system
                )

            st.session_state.chat_history.append({
                "q": question,
                "a": answer,
                "docs": docs
            })

            # clear input by rerun trick
            st.rerun()