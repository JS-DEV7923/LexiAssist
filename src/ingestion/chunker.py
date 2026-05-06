from __future__ import annotations


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[dict]:
    clean = " ".join(text.split())
    if not clean:
        return []
    chunks: list[dict] = []
    start = 0
    chunk_id = 0
    step = max(chunk_size - overlap, 1)
    while start < len(clean):
        end = min(start + chunk_size, len(clean))
        content = clean[start:end]
        chunks.append(
            {
                "chunk_id": chunk_id,
                "text": content,
                "source_span": {"start_char": start, "end_char": end},
            }
        )
        chunk_id += 1
        start += step
    return chunks
