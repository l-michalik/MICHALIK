# 🚀 Retrieval Augmented Generation

## 🛠️ Technologies Used

[LLaMA2] [FAISS] [OpenAI] [LangChain]

---

## 📦 Project-by-Project Breakdown

### Project 1 (End to End RAG Pipeline): 
- **Goal**: Enable LLMs to generate responses based on external data sources.
- **Key Learnings**: RAG integrates retrieval with generation using vector similarity.
- **Technologies**: Embedding models and vector databases must be dimensionally aligned.
- **Takeaways**: Retrieval quality directly impacts the accuracy of generated responses.

### Project 2 (RAG Architecture in Depth)
- **Goal**: Explore the components and techniques behind modern RAG systems.
- **Key Learnings**: Understanding various retrieval strategies enhances response quality and domain adaptability.
- **Technologies**: Sparse (TF-IDF, BM25), Dense (DPR, SBERT), Hybrid, Ensemble, Re-ranking (MonoT5, BGE-Reranker)
- **Takeaways**: The right combination of retrieval techniques improves relevance and factual grounding.

### Project 3 (Rag Cosine similiarity)

- **Goal**: Match a user query to the most relevant activity description using cosine similarity.
- **Key Learnings**: Applying vector-based similarity improves text relevance matching.
- **Technologies**: Python, Counter, math, requests, LLaMA2 via Ollama API
- **Takeaways**: Combining cosine similarity with local AI models enables efficient recommendations.

### Project 4 (Rag Applciation with FAISS)

- **Goal**: Implement a Retrieval-Augmented Generation (RAG) pipeline for question answering using a local document and OpenAI's GPT model.
- **Key Learnings**: How to combine document retrieval with language models for context-aware responses.
- **Technologies**: LangChain, OpenAI API, FAISS, dotenv
- **Takeaways**: RAG improves answer accuracy by grounding responses in relevant source data.

---

## 🔄 Shared Concepts & Reusable Patterns

- [01] Modular pipeline for chunking, embedding, retrieval, and generation
- [02] Use of ensemble retrieval with cross-encoder re-ranking for precision
- [03] Vector comparison using word frequency.
- [04] Text chunking, vector embeddings, similarity search, prompt templating

---

## Features

- [01] Dynamic, context-aware responses based on live external data
- [02] Support for hybrid retrieval strategies (sparse + dense + structured)
- [03] Streams AI response based on best-matched document.
- [04] FAISS vector index for retrieval

---