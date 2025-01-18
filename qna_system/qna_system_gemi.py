import psycopg2
import google.generativeai as genai
import streamlit as st
from psycopg2.extensions import register_adapter, AsIs
import os
from dotenv import load_dotenv
import requests  # Assuming Gemini API uses HTTP requests

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"  # Replace with the actual Gemini API URL

# PostgreSQL connection
try:
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB_NAME"),
        user=os.getenv("POSTGRES_DB_USER"),
        password=os.getenv("POSTGRES_DB_PASSWORD"),
        host=os.getenv("POSTGRES_DB_HOST"),
        port=os.getenv("POSTGRES_DB_PORT")
    )
    cursor = conn.cursor()
    st.success("✅ Successfully connected to PostgreSQL database")
except Exception as e:
    st.error(f"❌ Database connection failed: {e}")
    st.stop()

# Sample document chunks
documents = [
    "Artificial Intelligence (AI) is the simulation of human intelligence by machines, enabling them to perform tasks that typically require human cognition, such as learning, reasoning, problem-solving, and decision-making."
    "AI encompasses a range of technologies, including machine learning, natural language processing, and computer vision. "
    "It is widely used in applications like virtual assistants, recommendation systems, autonomous vehicles, and healthcare diagnostics, revolutionizing industries and enhancing daily life."
]

st.title("🔍 Interactive Q&A System with Retrieval-Augmented Generation")
st.write("This application demonstrates the steps in a **Q&A system** using Gemini embeddings and PostgreSQL.")

## Step 1: Document Chunking
st.header("📌 Step 1: Document Chunking")
st.write("Here are the document chunks that will be used for context:")

for i, doc in enumerate(documents, start=1):
    st.write(f"**Chunk {i}:** {doc}")

# Generate and store embeddings in PostgreSQL
embeddings = []

## Step 2: Generate and Display Embeddings
st.header("📌 Step 2: Generating Embeddings")
st.write("Each document chunk is converted into an embedding vector.")


def generate_embedding_gemini(text):
    """Generates embeddings using Gemini API."""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        data = {
            "content": {"parts": [{"text": text}]}
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        st.write("🔍 API Response:", result)  # Debugging output

        # Extract the embedding vector
        if "embedding" in result and "values" in result["embedding"]:
            embedding_values = result["embedding"]["values"]
            st.write(f"✅ Embedding length: {len(embedding_values)}")

            return embedding_values  # Ensure it's correct length

        st.error("❌ No embedding found in API response")
        return None

    except requests.exceptions.HTTPError as http_err:
        st.error(f"❌ HTTP error: {http_err}")
    except Exception as e:
        st.error(f"❌ Error generating embedding: {e}")

    return None




for doc in documents:
    try:
        # Generate embeddings
        embedding = generate_embedding_gemini(doc)
        if embedding:
            embeddings.append(embedding)

            # Insert the document text and embedding into the database
            cursor.execute(
                "INSERT INTO document_chunks (content, embeddings) VALUES (%s, %s::vector)",
                (doc, embedding)
            )
            st.write(f"✅ **Embedding for chunk:** `{doc[:50]}...` (truncated for display)")
            st.write(embedding)

    except Exception as e:
        st.error(f"❌ Error generating/storing embedding: {e}")

# Commit embeddings to database
conn.commit()

## Step 3: Retrieving Relevant Chunks for a Question
st.header("📌 Step 3: Retrieve Relevant Chunks")
question = st.text_input("🔍 **Enter your question:**")


def get_relevant_chunks(question, top_b=3):
    """Retrieves the most relevant chunks from PostgreSQL based on similarity."""
    try:
        # Generate embedding for the question
        question_embedding = generate_embedding_gemini(question)
        if not question_embedding:
            return []

        # Query the top-N most similar chunks using pgvector's similarity operator
        cursor.execute("""
            SELECT content
            FROM document_chunks
            ORDER BY embeddings <=> %s::vector
            LIMIT %s
        """, (question_embedding, top_b))

        # Fetch the results
        relevant_chunks = [row[0] for row in cursor.fetchall()]
        return relevant_chunks

    except Exception as e:
        st.error(f"❌ Error retrieving relevant chunks: {e}")
        return []


if question:
    st.write(f"📝 **Embedding for the question:** `{question}`")
    
    try:
        # Retrieve relevant chunks
        relevant_chunks = get_relevant_chunks(question)

        st.write("### 🔎 Top Relevant Chunks Retrieved:")
        for i, chunk in enumerate(relevant_chunks, start=1):
            st.write(f"{i}. {chunk}")

        ## Step 4: Generate and Display Answer using Gemini API
        st.header("📌 Step 4: Generate Answer Using Gemini API")
        context = "\n".join(f"{i+1}. {chunk}" for i, chunk in enumerate(relevant_chunks))
        prompt = f"Using the following information:\n {context}\nAnswer the question: {question}"

        # Configure Gemini API
        genai.configure(api_key=GEMINI_API_KEY)

        # Initialize the Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Generate answer using Gemini API
        response = model.generate_content(prompt)

        # Extract and display the answer
        answer = response.text
        st.write("**💡 Generated Answer:**")
        st.write(answer)

    except Exception as e:
        st.error(f"❌ Error generating answer: {e}")

# Close database connection
cursor.close()
conn.close()
st.success("✅ Database connection closed successfully.")
