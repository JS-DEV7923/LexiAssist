# LexiAssist v1

LexiAssist is a local-first legal document QA application built with Streamlit, ChromaDB, and pluggable LLM providers.  
It uses a Retrieval-Augmented Generation (RAG) pipeline to answer user questions with citation-linked evidence from uploaded PDF/DOCX files.

## Features

- Authentication with hashed passwords and isolated user data.
- PDF/DOCX ingestion, chunking, embedding, and vector indexing.
- Provider-abstracted LLM + embeddings (Gemini or Groq for LLM; Gemini or local for embeddings).
- Citation-based legal QA over user-owned documents only.
- Knowledge base management (upload/list/delete) and chat history.

## Tech Stack

- Python
- Streamlit
- ChromaDB
- Gemini API (`google-generativeai`) or Groq API (`groq`)
- SQLite

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Configure environment:
   - `cp .env.example .env`
   - For Groq-only setup, use:
     - `LLM_PROVIDER=groq`
     - `EMBEDDING_PROVIDER=local`
     - `GROQ_API_KEY=<your_key>`
4. Run the app:
   - `streamlit run app.py`

## Environment Variables

See `.env.example` for defaults. Key values:

- `LLM_PROVIDER` (default: `gemini`)
- `EMBEDDING_PROVIDER` (default: `gemini`)
- `GEMINI_API_KEY`
- `GEMINI_CHAT_MODEL`
- `GEMINI_EMBED_MODEL`
- `GROQ_API_KEY`
- `GROQ_CHAT_MODEL`
- `LOCAL_EMBEDDING_MODEL`
- `CHROMA_PERSIST_DIR`
- `METADATA_DB_PATH`
- `UPLOAD_DIR`
- `MAX_UPLOAD_MB`
- `CHUNK_SIZE`
- `CHUNK_OVERLAP`
- `RETRIEVAL_TOP_K`

## Security Notes

- Passwords are hashed using bcrypt via `passlib`.
- User isolation is enforced in metadata queries and vector retrieval filters.
- Uploaded files are stored locally and not shared between users.
- File type and file size are validated before ingestion.

## Tests

Run:

- `pytest -q`

Current test coverage includes chunking behavior, auth flow, retriever filters, and chat fallback behavior.
