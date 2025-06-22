## 🔠 What Does RAG Stand For?

**RAG** = **Retrieval-Augmented Generation**

It’s a framework that augments language model outputs with external data sources by:
- **Retrieving** relevant documents (from a database or vector store),
- **Augmenting** the prompt with these documents,
- **Generating** a final answer using a language model (e.g., GPT or LLaMA).

---

## 🚀 What Is RAG?

**RAG** allows LLMs to access information beyond their training data by dynamically fetching relevant documents at inference time. This avoids hallucinations and keeps the model’s output grounded in real, up-to-date facts — especially useful for domain-specific or time-sensitive applications.

---

## 🔁 What Is the Flow of RAG?

1. **Input Question**: User submits a query.
2. **Chunking**: Documents are split into manageable pieces.
3. **Embedding**: Chunks are transformed into vector representations.
4. **Retrieval**: Similar vectors are retrieved using similarity search.
5. **Augmentation**: Retrieved chunks are appended to the user’s question.
6. **Generation**: The augmented input is sent to an LLM to generate a final answer.

---

## 🧠 RAG Embeddings

- Embeddings are numerical vector representations of text.
- Used for comparing the semantic similarity between queries and documents.
- Generated using models like Sentence Transformers, OpenAI embeddings, or HuggingFace Transformers.

---

## 📏 RAG Dimensions

- The **embedding dimension** refers to the length of the vector (e.g., 384, 768, 1536).
- Higher dimensions can capture more detail but require more computation and storage.
- Must match the expected dimension of your vector store.

---

## 🔍 Similarity in RAG

RAG systems retrieve the most **semantically similar** chunks using:
- **Cosine similarity**
- **Euclidean distance**
- **Dot product**

These scores determine which chunks are relevant enough to augment the query.

---

## 🧩 RAG Pipeline Summary

| Step         | Description                                    |
|--------------|------------------------------------------------|
| Chunking     | Split large docs into smaller pieces           |
| Embedding    | Convert chunks into vector format              |
| Storage      | Save embeddings into a vector database         |
| Retrieval    | Search database for similar vectors            |
| Augmentation | Combine retrieved chunks with user query       |
| Generation   | Feed to LLM for final answer                   |

---

## 📦 Chunk Size

- Determines the **length of text** per chunk (e.g., 256 tokens, 500 words).
- Too small: loss of context.  
- Too large: harder to retrieve accurately and may exceed token limits.

---

## 🪓 Chunking Strategies

- **Sliding window**: Overlapping chunks for context retention.
- **Recursive splitting**: Breaks by sentence/paragraph using fallback rules.
- **Fixed-size**: Simple uniform chunk lengths.

Best strategy depends on use case and document structure.

---

## 🗃️ Databases for RAG

Popular vector databases used in RAG:
- **FAISS** (Facebook AI Similarity Search) – fast and lightweight.
- **Chroma** – simple, local vector DB for prototyping.
- **Weaviate** – scalable, supports metadata filters.
- **Pinecone** – managed, production-ready vector DB.
- **Qdrant** – open-source, great for hybrid search.
- **Milvus** – scalable and distributed.
