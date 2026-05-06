from __future__ import annotations

from io import BytesIO

from docx import Document
from pypdf import PdfReader


def parse_pdf_bytes(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    pages: list[str] = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return "\n".join(pages).strip()


def parse_docx_bytes(file_bytes: bytes) -> str:
    document = Document(BytesIO(file_bytes))
    return "\n".join(p.text for p in document.paragraphs).strip()


def parse_uploaded_file(file_name: str, file_bytes: bytes) -> str:
    lowered = file_name.lower()
    if lowered.endswith(".pdf"):
        return parse_pdf_bytes(file_bytes)
    if lowered.endswith(".docx"):
        return parse_docx_bytes(file_bytes)
    raise ValueError("Only PDF and DOCX are supported")
