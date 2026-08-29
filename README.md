# 📚 Simple RAG Chatbot

A beginner-friendly Retrieval-Augmented Generation (RAG) chatbot that allows users to ask questions about information stored in a PDF document.

This project uses Gemini 3 Flash as the language model and does not use OpenAI.

---

## 🚀 Technologies Used

- Python: Main programming language
- Streamlit: Creates the web interface
- PyPDF: Extracts text from PDF files
- Sentence Transformers: Creates text embeddings
- ChromaDB: Stores and searches embeddings
- Gemini 3 Flash: Generates answers
- python-dotenv: Loads the Gemini API key

---

## 🧠 What is RAG?

RAG (Retrieval-Augmented Generation) combines document retrieval with an AI language model.

Instead of asking Gemini to answer a question only from its general knowledge, this project first searches the user's document for relevant information.

---

## 🔍 How the System Works

### 1. Loading the Gemini API Key

The Gemini API key is stored in an environment file rather than directly inside the Python source code.

This helps protect sensitive credentials and prevents accidentally exposing the API key on GitHub.

### 2. Gemini Model

The project uses Gemini 3 Flash Preview as the Large Language Model.

Gemini is responsible for generating the final answer using the relevant information retrieved from the PDF.

### 📄 3. Reading the PDF

The PDF is processed using PyPDF.

The system reads each page and extracts the available text.

The process is:

**PDF → Pages → Extracted Text**

The extracted text is then passed to the next stage.

### ✂️ 4. Splitting Text into Chunks

Large documents are divided into smaller sections called chunks.

The process is:

**Large Document → Full Text → Multiple Smaller Chunks**

Chunking makes it easier to search for specific information instead of processing the entire document for every question.

### 🔢 5. Creating Embeddings

Each text chunk is converted into a numerical representation called an embedding using Sentence Transformers.

Embeddings represent the semantic meaning of text.

This allows the system to identify text that is similar in meaning, even when the exact words are different.

### 🗄️ 6. Storing Information in ChromaDB

The text chunks and their embeddings are stored in ChromaDB, which acts as the vector database.

ChromaDB allows the system to efficiently search for chunks that are semantically similar to the user's question.

The stored information can be thought of as:

**Text Chunk → Embedding → Vector Database**

### 🔎 7. Retrieving Relevant Information

When the user asks a question, the question is converted into an embedding.

The embedding is compared with the embeddings stored in ChromaDB.

The system retrieves the most relevant chunks from the PDF.

This is the Retrieval part of RAG.

### 🤖 8. Generating the Answer with Gemini

The retrieved chunks are provided to Gemini together with the user's question.

Gemini uses this context to generate the final response.

The system instructs Gemini to answer using the retrieved document information.

If the required information cannot be found in the retrieved context, the chatbot can indicate that the answer is not available in the document.

This is the Generation part of RAG.

---

## 📚 Concepts Practiced
Retrieval-Augmented Generation (RAG)
Large Language Models (LLMs)
Gemini API
PDF text extraction
Text chunking
Embeddings
Vector databases
Semantic search
Similarity search
Context retrieval
Prompt construction
Streamlit
Environment variables
Python project structure

---

## ⭐ Project Goal

The goal of this project is to understand the fundamental concepts behind Retrieval-Augmented Generation by building a simple RAG application from scratch using Python, ChromaDB, Sentence Transformers, Streamlit, and Gemini.