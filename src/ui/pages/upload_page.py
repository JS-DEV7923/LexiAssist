from __future__ import annotations

import streamlit as st

from src.chat.service import ChatService
from src.storage.metadata_db import MetadataDB


def render_upload_page(chat_service: ChatService, metadata_db: MetadataDB, user_id: str, max_upload_mb: int) -> None:
    st.subheader("Knowledge Base")
    uploaded = st.file_uploader("Upload legal document", type=["pdf", "docx"])
    if uploaded is not None:
        size_mb = uploaded.size / (1024 * 1024)
        if size_mb > max_upload_mb:
            st.error(f"File exceeds max size ({max_upload_mb} MB)")
        elif st.button("Index document"):
            try:
                chat_service.ingest_document(
                    user_id=user_id,
                    file_name=uploaded.name,
                    file_bytes=uploaded.getvalue(),
                )
                st.success("Document indexed")
                st.rerun()
            except Exception as exc:
                st.error(str(exc))

    docs = metadata_db.list_documents(user_id=user_id)
    st.markdown("### Uploaded Documents")
    if not docs:
        st.info("No documents uploaded yet.")
    for doc in docs:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(doc["name"])
        with col2:
            if st.button("Delete", key=f"delete_{doc['id']}"):
                chat_service.delete_document(user_id=user_id, doc_id=doc["id"])
                st.rerun()
