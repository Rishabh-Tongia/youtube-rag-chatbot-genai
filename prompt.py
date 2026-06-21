from langchain_core.prompts import ChatPromptTemplate


def get_prompt():

    template = """
    You are a helpful AI assistant.
    Answer ONLY using the provided context.
    If the answer is not present,
    say:
    "I couldn't find this information in the video."
    Context:
    {context}
    Question:
    {question}
    Answer:
    """
    return ChatPromptTemplate.from_template(template)