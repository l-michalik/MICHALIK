from db.weaviate_client import create_schema_if_missing, get_weaviate_client
from generator.rag_pipeline import query_index, generate_answer
from db.upsert import upsert_documents

def main():
    client = get_weaviate_client()
    
    create_schema_if_missing(client)

    docs = [
        {"content": "LangChain v0.1.6 deprecated 'load_chain'.", "source": "LangChain docs"},
        {"content": "Transformers now use 'AutoModel' instead of 'BertModel'.", "source": "HuggingFace changelog"},
        {"content": "FastAPI error 'object not subscriptable' often comes from incorrect Pydantic model usage.", "source": "Stack Overflow"},
    ]
    
    upsert_documents(docs)

    print("❓ Ask your AI Troubleshooter a question:")
    question = input("> ")

    chunks = query_index(question)
    answer = generate_answer(question, chunks)

    print(answer)
    
    client.close()

if __name__ == "__main__":
    main()
