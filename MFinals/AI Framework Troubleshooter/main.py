from db.weaviate_client import get_weaviate_client, create_schema_if_missing
from generator.rag_pipeline import query_index, generate_answer
from retriever.embedder import embed_text

def embed_sample_docs():
    docs = [
        {"content": "LangChain v0.1.6 deprecated 'load_chain'.", "source": "LangChain docs"},
        {"content": "Transformers now use 'AutoModel' instead of 'BertModel'.", "source": "HuggingFace changelog"},
        {"content": "FastAPI error 'object not subscriptable' often comes from incorrect Pydantic model usage.", "source": "Stack Overflow"},
    ]

    client = get_weaviate_client()
    collection = client.collections.get("DocChunk")

    for doc in docs:
        vector = embed_text(doc["content"])
        collection.data.insert(
            properties={
                "content": doc["content"],
                "source": doc["source"]
            },
            vector=vector
        )

def main():
    client = get_weaviate_client()
    
    create_schema_if_missing(client)

    print("📚 Indexing example docs...")
    embed_sample_docs()

    print("❓ Ask your AI Troubleshooter a question:")
    question = input("> ")

    chunks = query_index(question)
    answer = generate_answer(question, chunks)

    print(answer)
    
    client.close()

if __name__ == "__main__":
    main()
