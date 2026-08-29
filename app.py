import streamlit as st
from rag import ask_question


# Page configuration
st.set_page_config(
    page_title="Simple RAG Chatbot",
    page_icon="📚",
    layout="centered"
)


# Title
st.title("📚 Simple RAG Chatbot")

st.write(
    "Ask questions about the information in your PDF."
)


# Question input
question = st.text_input(
    "💬 Enter your question:"
)


# Ask button
if st.button("🔍 Ask"):

    if question.strip():

        with st.spinner("Searching the document..."):

            try:
                answer = ask_question(question)

                st.subheader("🤖 Answer")

                st.write(answer)

            except Exception as e:

                st.error(f"Error: {e}")

    else:

        st.warning("Please enter a question.")