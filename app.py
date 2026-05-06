from __future__ import annotations

import streamlit as st

from src.auth.service import AuthService
from src.auth.store import AuthStore
from src.chat.service import ChatService
from src.config.settings import load_settings
from src.llm.factory import build_providers
from src.retrieval.retriever import Retriever
from src.retrieval.vector_store import ChromaVectorStore
from src.storage.metadata_db import MetadataDB
from src.ui.pages.auth_page import render_auth_page
from src.ui.pages.chat_page import render_chat_page
from src.ui.pages.upload_page import render_upload_page


def build_services():
    settings = load_settings()
    metadata_db = MetadataDB(settings.metadata_db_path)
    auth_service = AuthService(AuthStore(metadata_db))
    embedding_provider, llm_provider = build_providers(settings)
    vector_store = ChromaVectorStore(settings.chroma_persist_dir)
    retriever = Retriever(vector_store=vector_store, embedding_provider=embedding_provider)
    chat_service = ChatService(
        metadata_db=metadata_db,
        vector_store=vector_store,
        retriever=retriever,
        llm_provider=llm_provider,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        top_k=settings.retrieval_top_k,
        upload_dir=settings.upload_dir,
    )
    return settings, metadata_db, auth_service, chat_service


def main() -> None:
    st.set_page_config(page_title="LexiAssist", layout="wide")
    settings, metadata_db, auth_service, chat_service = build_services()

    if "user" not in st.session_state:
        render_auth_page(auth_service)
        return

    user = st.session_state["user"]
    sidebar = st.sidebar
    sidebar.title("Session")
    sidebar.write(user["email"])
    if sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    tab_upload, tab_chat = st.tabs(["Knowledge Base", "Chat"])
    with tab_upload:
        render_upload_page(
            chat_service=chat_service,
            metadata_db=metadata_db,
            user_id=user["id"],
            max_upload_mb=settings.max_upload_mb,
        )
    with tab_chat:
        render_chat_page(chat_service=chat_service, metadata_db=metadata_db, user_id=user["id"])


if __name__ == "__main__":
    main()
