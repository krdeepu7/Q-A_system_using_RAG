# Interactive Q&A System with Retrieval-Augmented Generation

This project is an **Interactive Q&A System** that leverages **PostgreSQL**, **Gemini embeddings**, and **Streamlit** to implement a Retrieval-Augmented Generation (RAG) approach for question answering.

## Features

- **Document Chunking**: Breaks down documents into manageable chunks for embedding and retrieval.
- **Embedding Generation**: Uses the Gemini API to generate embeddings for the document chunks and questions.
- **Vector Storage**: Stores embeddings in a PostgreSQL database with support for vector similarity operations (e.g., `pgvector`).
- **Relevant Chunk Retrieval**: Queries the most relevant document chunks based on similarity to the user's question.
- **Answer Generation**: Uses the Gemini Generative AI API to generate answers based on retrieved chunks.
- **Streamlit Frontend**: Provides a user-friendly interface for interacting with the system.

---

## Prerequisites

- Python 3.8+
- PostgreSQL database with `pgvector` extension installed
- Gemini API access and key
- `.env` file containing environment variables:
  ```env
  GEMINI_API_KEY=your_gemini_api_key
  POSTGRES_DB_NAME=your_db_name
  POSTGRES_DB_USER=your_db_user
  POSTGRES_DB_PASSWORD=your_db_password
  POSTGRES_DB_HOST=your_db_host
  POSTGRES_DB_PORT=your_db_port
  ```

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/interactive-qa-system.git
   cd interactive-qa-system
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows: .\env\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up PostgreSQL**
   - Create a database and enable the `pgvector` extension:
     ```sql
     CREATE DATABASE your_db_name;
     \c your_db_name
     CREATE EXTENSION vector;
     ```
   - Create the `document_chunks` table:
     ```sql
     CREATE TABLE document_chunks (
       id SERIAL PRIMARY KEY,
       content TEXT,
       embeddings VECTOR(768)
     );
     ```

5. **Configure Environment Variables**
   - Add the required variables to a `.env` file (see above).

6. **Run the Application**
   ```bash
   streamlit run app.py
   ```

---

## Usage

1. **Document Chunking**: View the predefined document chunks in the Streamlit app.
2. **Embedding Generation**: Automatically generate embeddings for the chunks and store them in the PostgreSQL database.
3. **Ask a Question**: Input a question in the app. The system retrieves relevant chunks and generates an answer using the Gemini API.
4. **Answer Display**: The generated answer is displayed alongside the relevant chunks.

---

## Project Structure

```
interactive-qa-system/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env                # Environment variables
└── README.md           # Project documentation
```

---

## Dependencies

- [psycopg2](https://pypi.org/project/psycopg2/): PostgreSQL database adapter for Python.
- [streamlit](https://streamlit.io/): Framework for creating interactive web applications.
- [google.generativeai](https://developers.google.com/): Library for accessing Gemini API.
- [dotenv](https://pypi.org/project/python-dotenv/): For managing environment variables.
- [requests](https://pypi.org/project/requests/): For making HTTP requests to the Gemini API.

---

## Troubleshooting

- **Database Connection Issues**:
  - Ensure PostgreSQL is running and the credentials in `.env` are correct.
  - Verify the `pgvector` extension is installed.

- **Gemini API Errors**:
  - Check the API key and URL in the `.env` file.
  - Confirm your API key has the necessary permissions.

- **Embedding Errors**:
  - Ensure the `document_chunks` table schema matches the expected structure.
  - Validate the embedding size matches the vector column dimensions.

---

## Acknowledgments

- [Google Generative AI](https://developers.google.com/): For the Gemini API.
- [Streamlit](https://streamlit.io/): For the interactive interface.
- [PostgreSQL](https://www.postgresql.org/): For data storage and vector operations.

Feel free to contribute or raise issues in the repository! 🚀

# Output should look like similar to this.
![qna_system_gemi_page-0001](https://github.com/user-attachments/assets/e8e02a24-0153-42ce-883e-5ea829fcedb2)

![qna_system_gemi_page-0002](https://github.com/user-attachments/assets/11aea195-d483-4060-93ac-9a045382167c)

![qna_system_gemi_page-0003](https://github.com/user-attachments/assets/a65d2b72-7303-4716-8726-0c2a81d8fc9a)

