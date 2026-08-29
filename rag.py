import os

from dotenv import load_dotenv
from google import genai

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

import chromadb


# --------------------------------------------------
# 1. Load environment variables
# --------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Please add it to your .env file."
    )


# --------------------------------------------------
# 2. Gemini configuration
# --------------------------------------------------

MODEL_NAME = "gemini-3-flash-preview"

client = genai.Client(
    api_key=API_KEY
)


# --------------------------------------------------
# 3. Embedding model
# --------------------------------------------------

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# --------------------------------------------------
# 4. Load PDF
# --------------------------------------------------

PDF_PATH = "documents/notes.pdf"


def load_pdf(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# --------------------------------------------------
# 5. Create text chunks
# --------------------------------------------------

def create_chunks(text, chunk_size=500):

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):

        chunk = " ".join(
            words[i:i + chunk_size]
        )

        if chunk.strip():
            chunks.append(chunk)

    return chunks


# --------------------------------------------------
# 6. Create ChromaDB
# --------------------------------------------------

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="pdf_documents"
)


# --------------------------------------------------
# 7. Process PDF and store embeddings
# --------------------------------------------------

def process_document():

    text = load_pdf(PDF_PATH)

    if not text.strip():
        raise ValueError(
            "No text could be extracted from the PDF."
        )

    chunks = create_chunks(text)

    embeddings = embedding_model.encode(
        chunks
    )

    # Avoid adding the same chunks repeatedly
    existing_data = collection.get()

    if len(existing_data["ids"]) == 0:

        collection.add(
            documents=chunks,
            embeddings=embeddings.tolist(),
            ids=[
                f"chunk_{i}"
                for i in range(len(chunks))
            ]
        )

    return len(chunks)


# --------------------------------------------------
# 8. Retrieve relevant documents
# --------------------------------------------------

def search_documents(question, n_results=3):

    question_embedding = embedding_model.encode(
        [question]
    )

    results = collection.query(
        query_embeddings=question_embedding.tolist(),
        n_results=n_results
    )

    return results["documents"][0]


# --------------------------------------------------
# 9. Generate answer using Gemini
# --------------------------------------------------

def generate_answer(question, context):

    prompt = f"""
You are a helpful document assistant.

Answer the user's question using ONLY the information
provided in the context below.

Do not use outside knowledge.

If the answer cannot be found in the context,
say:

"I could not find the answer in the document."

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text


# --------------------------------------------------
# 10. Complete RAG pipeline
# --------------------------------------------------

def ask_question(question):

    # Make sure the PDF has been processed
    if collection.count() == 0:

        process_document()

    # Retrieve relevant chunks
    results = search_documents(question)

    # Combine chunks into context
    context = "\n\n".join(results)

    # Generate answer with Gemini
    answer = generate_answer(
        question,
        context
    )

    return answer