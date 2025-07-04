from db.weaviate_client import get_weaviate_client
from retriever.embedder import embed_text

def upsert_documents(docs: list):
    client = get_weaviate_client()
    collection = client.collections.get("DocChunk")

    existing = collection.query.bm25(query="*", limit=1000).objects
    existing_contents = {obj["properties"]["content"] for obj in existing}

    for doc in docs:
        if doc["content"] in existing_contents:
            print(f"⚠️ Skipping duplicate: {doc['content'][:60]}")
            continue

        vector = embed_text(doc["content"])
        collection.data.insert(
            properties={
                "content": doc["content"],
                "source": doc["source"]
            },
            vector=vector
        )
        print(f"✅ Inserted: {doc['content'][:60]}")
