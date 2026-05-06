from __future__ import annotations

import json

import streamlit as st

from src.chat.service import ChatService
from src.storage.metadata_db import MetadataDB


def render_chat_page(chat_service: ChatService, metadata_db: MetadataDB, user_id: str) -> None:
    st.subheader("Legal QA Chat")
    docs = metadata_db.list_documents(user_id=user_id)
    doc_options = {d["name"]: d["id"] for d in docs}
    selected_names = st.multiselect("Limit to documents (optional)", options=list(doc_options.keys()))
    selected_ids = [doc_options[name] for name in selected_names] if selected_names else None

    question = st.text_area("Ask a question about your documents")
    if st.button("Ask"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            response = chat_service.ask(user_id=user_id, question=question.strip(), doc_ids=selected_ids)
            st.markdown("### Answer")
            st.write(response["answer"])
            st.markdown("### Citations")
            if not response["citations"]:
                st.info("No citations available.")
            for c in response["citations"]:
                with st.expander(f"[{c['index']}] {c['file_name']} (chunk {c['chunk_id']})"):
                    st.write(c["excerpt"])

    st.markdown("### Recent Chat History")
    for row in metadata_db.list_chats(user_id=user_id, limit=20):
        st.markdown(f"**Q:** {row['question']}")
        st.markdown(f"**A:** {row['answer']}")
        citations = json.loads(row["citations_json"])
        if citations:
            st.caption(
                "Citations: "
                + ", ".join(f"[{c['index']}] {c['file_name']}#chunk{c['chunk_id']}" for c in citations)
            )
