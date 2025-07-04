from db.weaviate_client import get_weaviate_client
from retriever.embedder import embed_text
from generator.llm_runner import call_openai_llm

def query_index(question: str) -> list:
    client = get_weaviate_client()
    vector = embed_text(question)
    collection = client.collections.get("DocChunk")
    results = collection.query.near_vector(vector, limit=4)
    return results.objects

def generate_answer(question: str, context_chunks: list) -> str:
    context = "\n".join([
        f"• {chunk.properties['content']} (source: {chunk.properties.get('source', 'unknown')})"
        for chunk in context_chunks
    ])

    system_prompt = (
        "You are an expert AI developer assistant. "
        "Use the provided context (from documentation, forums, and GitHub) "
        "to answer the user's question truthfully and concisely. "
        "Do not guess or invent facts. Include code examples if helpful."
    )

    user_prompt = (
        f"Question:\n{question}\n\n"
        f"Context:\n{context}\n\n"
        f"Answer the question using ONLY the context above."
    )

    answer = call_openai_llm(system_prompt, user_prompt)

    return f"""
================= 💬 Developer Question =================

{question}

================= 🤖 OpenAI Answer =======================

{answer}
"""
