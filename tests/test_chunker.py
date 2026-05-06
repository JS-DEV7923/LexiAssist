from src.ingestion.chunker import chunk_text


def test_chunk_text_returns_overlapping_chunks():
    text = "a" * 1000
    chunks = chunk_text(text=text, chunk_size=300, overlap=50)
    assert len(chunks) >= 3
    assert chunks[0]["source_span"]["start_char"] == 0
    assert chunks[1]["source_span"]["start_char"] == 250
