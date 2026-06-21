import streamlit as st
from src.utils.time_utils import format_timestamp


from src.chatbot import (
    build_rag_system,
    ask_question
)

st.set_page_config(
    page_title="YouTube RAG Chatbot"
)

st.title("🎥 YouTube RAG Chatbot")

url = st.text_input(
    "YouTube URL"
)

if st.button("Load Video"):

    with st.spinner("Processing Video..."):

        rag_system = build_rag_system(url)

        st.session_state.rag_system = rag_system
        st.session_state.video_loaded = True

    st.success("Video Loaded Successfully!")

if st.session_state.get("video_loaded"):

    question = st.text_input(
        "Ask a Question"
    )

    if st.button("Ask"):

        with st.spinner("Generating Answer..."):

            answer, docs = ask_question(
                question,
                st.session_state.rag_system
            )

        st.subheader("Answer")

        st.write(answer)

        st.subheader("Sources")

        for doc in docs:

            start_time = format_timestamp(
                doc.metadata["start_time"]
            )

            end_time = format_timestamp(
                doc.metadata["end_time"]
            )

            st.write(
                f"📌 {start_time} - {end_time}"
            )