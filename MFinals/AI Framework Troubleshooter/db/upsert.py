import hashlib
from db.weaviate_client import get_weaviate_client
from retriever.embedder import embed_text

def hash_text(text: str) -> str:
    return hashlib.sha256(text.strip().encode()).hexdigest()

def upsert_documents(docs: list):
    client = get_weaviate_client()
    collection = client.collections.get("DocChunk")

    print("🔎 Fetching existing content hashes from Weaviate...")
    existing = collection.query.bm25(query="*", limit=1000).objects
    existing_hashes = {
        obj.properties.get("content_hash")
        for obj in existing
        if obj.properties.get("content_hash")
    }

    upserted_count = 0

    for doc in docs:
        content = doc["content"]
        content_hash = hash_text(content)

        if content_hash in existing_hashes:
            print(f"⚠️ Skipping duplicate: {content[:60]}")
            continue

        vector = embed_text(content)
        collection.data.insert(
            properties={
                "content": content,
                "source": doc["source"],
                "content_hash": content_hash
            },
            vector=vector
        )
        upserted_count += 1

    print(f"✅ Upserted {upserted_count} new documents to Weaviate.")
