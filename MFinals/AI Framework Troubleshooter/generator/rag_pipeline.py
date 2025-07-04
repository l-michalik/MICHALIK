import logging
from db.weaviate_client import get_weaviate_client
from retriever.embedder import embed_text
from generator.llm_runner import call_openai_llm
from generator.prompt_template import format_prompt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_keywords(question: str) -> list:
    return [word.lower() for word in question.split() if len(word) > 3]

def query_index(question: str) -> list:
    try:
        client = get_weaviate_client()
        vector = embed_text(question)
        collection = client.collections.get("DocChunk")
        results = collection.query.near_vector(vector, limit=8)
        chunks = results.objects

        logger.info(f"🔍 Retrieved {len(chunks)} chunks for question: '{question}'")

        keywords = extract_keywords(question)
        filtered = [
            c for c in chunks
            if any(k in c.properties.get("content", "").lower() for k in keywords)
        ]

        if not filtered:
            logger.warning("⚠️ No filtered chunks matched keywords. Using all retrieved chunks.")
        return filtered or chunks

    except Exception as e:
        logger.error(f"❌ Failed to query vector index: {e}")
        return []

def generate_answer(question: str, context_chunks: list) -> str:
    try:
        system_prompt, user_prompt = format_prompt(question, context_chunks)
        answer = call_openai_llm(system_prompt, user_prompt).strip()

        base_output = f"""
================= 💬 Developer Question =================
{question}

================= 🤖 OpenAI Answer =======================
{answer}
""".strip()

        if answer.lower() in {"i don't know", "i do not know", "no information available", "unknown"}:
            return base_output

        sources = {}
        for chunk in context_chunks:
            src = chunk.properties.get("source", "unknown")
            if src not in sources:
                sources[src] = len(sources) + 1

        reference_section = "\n".join(f"[{i}] {url}" for url, i in sources.items())

        return f"{base_output}\n\n================= 🔗 Sources ============================\n{reference_section}".strip()

    except Exception as e:
        logger.error(f"❌ Failed to generate answer: {e}")
        return f"""
================= 💬 Developer Question =================
{question}

================= 🤖 OpenAI Answer =======================
An error occurred while generating the answer. Please try again later.
""".strip()
