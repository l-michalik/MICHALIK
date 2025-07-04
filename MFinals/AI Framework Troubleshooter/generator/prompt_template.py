def format_prompt(question: str, context_chunks: list) -> tuple[str, str]:
    context = "\n\n".join(
        f"- {chunk.properties['content']} (source: {chunk.properties.get('source', 'unknown')})"
        for chunk in context_chunks
    )

    system_prompt = (
        "You are an expert AI developer assistant. "
        "Use the provided context (from documentation, forums, GitHub) "
        "to answer the user's question. Be precise, helpful, and include code examples if relevant. "
        "Do NOT make up information. Only use what's in the context."
        "If you don't know the answer,your whole answear should be only 'I don't know'. "
    )

    user_prompt = (
        f"Question:\n{question}\n\n"
        f"Context:\n{context}\n\n"
        "Now provide a helpful, grounded answer using only the context above."
    )

    return system_prompt, user_prompt
