import logging
from db.weaviate_client import get_weaviate_client
from retriever.embedder import embed_text
from generator.llm_runner import call_openai_llm
from generator.prompt_template import format_prompt

logger = logging.getLogger(__name__)

def extract_keywords(question: str) -> list:
    return [word.lower() for word in question.split() if len(word) > 3]

def query_index(question: str) -> list:
    try:
        client = get_weaviate_client()
        vector = embed_text(question)
        collection = client.collections.get("DocChunk")
        results = collection.query.near_vector(vector, limit=15, certainty=0.7)
        chunks = results.objects

        print(f"🔍 Retrieved {len(chunks)} chunks for question: '{question}'")

        keywords = extract_keywords(question)

        def score(chunk):
            content = chunk.properties.get("content", "").lower()
            return sum(k in content for k in keywords)

        ranked = sorted(chunks, key=score, reverse=True)
        top_chunks = ranked[:5]

        return top_chunks or chunks

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

        if answer.lower() in {"i don't know", "i do not know", "no information available", "unknown", "i don't know."}:
            return base_output

        sources = {}
        source_versions = {}

        for chunk in context_chunks:
            src = chunk.properties.get("source", "unknown")
            version = chunk.properties.get("version", "").strip()
            if src not in sources:
                sources[src] = len(sources) + 1
                source_versions[src] = version or "unknown"

        reference_section = "\n".join(
            f"[{i}] {url} (v{source_versions[url]})"
            for url, i in sources.items()
        )

        return f"{base_output}\n\n================= 🔗 Sources ============================\n{reference_section}".strip()

    except Exception as e:
        logger.error(f"❌ Failed to generate answer: {e}")
        return f"""
================= 💬 Developer Question =================
{question}

================= 🤖 OpenAI Answer =======================
An error occurred while generating the answer. Please try again later.
""".strip()
