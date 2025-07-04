from db.weaviate_client import get_weaviate_client
from retriever.embedder import embed_text

def query_index(question: str) -> list:
    client = get_weaviate_client()
    vec = embed_text(question)

    doc_chunk = client.collections.get("DocChunk")
    results = doc_chunk.query.near_vector(vec, limit=3)

    client.close()
    return results.objects

def generate_answer(question: str, context_chunks: list) -> str:
    # Extract and format context snippets
    context_snippets = [
        f"• {chunk.properties['content']} (source: {chunk.properties.get('source', 'unknown')})"
        for chunk in context_chunks
    ]
    context_text = "\n".join(context_snippets)

    return f"""
================= 💬 Developer Question =================

{question}

================= 📚 Retrieved Context ==================

{context_text}

========================================================
"""
