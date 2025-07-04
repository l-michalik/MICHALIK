from db.weaviate_client import get_weaviate_client
from retriever.embedder import embed_text
from generator.llm_runner import call_openai_llm
from generator.prompt_template import format_prompt

def query_index(question: str) -> list:
    client = get_weaviate_client()
    vector = embed_text(question)
    collection = client.collections.get("DocChunk")
    results = collection.query.near_vector(vector, limit=4)
    return results.objects

def generate_answer(question: str, context_chunks: list) -> str:
    system_prompt, user_prompt = format_prompt(question, context_chunks)
    answer = call_openai_llm(system_prompt, user_prompt)

    return f"""
================= 💬 Developer Question =================

{question}

================= 🤖 OpenAI Answer =======================

{answer}
"""
