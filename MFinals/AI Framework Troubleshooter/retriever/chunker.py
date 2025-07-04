from typing import Dict, List

def chunk_text(text: str, max_tokens: int = 500) -> List[str]:
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) > max_tokens:
            if current:
                chunks.append(current.strip())
            current = para
        else:
            current += "\n\n" + para

    if current:
        chunks.append(current.strip())

    return [c for c in chunks if len(c.strip()) > 50]

def enrich_chunks(text: str, source: str) -> List[Dict]:
    from retriever.chunker import chunk_text
    import hashlib

    chunks = chunk_text(text)
    enriched = []

    for chunk in chunks:
        content_hash = hashlib.sha256(chunk.encode()).hexdigest()
        enriched.append({
            "content": chunk,
            "source": source,
            "content_hash": content_hash
        })

    return enriched
