# 🚀 Retrieval Augmented Generation

## 🛠️ Technologies Used

LLaMA2 | FAISS | OpenAI | LangChain | Weaviate | HuggingFace | Haystack | Gemini | Haystack | Pinecone | FastAPI

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

### Project 5 (RAG-Powered PDF QA with Weaviate)

- **Goal**: Enable question answering over a PDF by retrieving semantically relevant text using vector search and generating answers with a language model.
- **Key Learnings**: Retrieval-Augmented Generation improves answer quality by grounding outputs in contextually relevant source documents.
- **Technologies**: Python, Weaviate, LangChain, HuggingFace Transformers, Mistral via HuggingFaceHub
- **Takeaways**: Integrating vector databases with LLMs enables accurate and context-aware QA systems over unstructured documents.

### Project 6 (LLM-Powered RAG with LlamaIndex)

- **Goal**: Build a lightweight, file-based RAG system using LlamaIndex and Hugging Face-hosted models for local document QA.
- **Key Learnings**: LlamaIndex abstracts complex retrieval and generation workflows, making it fast to prototype production-grade RAG systems.
- **Technologies**: Python, LlamaIndex, HuggingFace Hub, Mistral-7B-Instruct, SentenceTransformers
- **Takeaways**: Lightweight RAG pipelines can be quickly implemented without a full vector database by using local indexing tools like LlamaIndex.

### Project 7 (LLM-Powered RAG with Gemini & LlamaIndex)

- **Goal**: Build a lightweight, file-based RAG system using LlamaIndex and Google Gemini for local document QA.
- **Key Learnings**: Gemini integrates smoothly with LlamaIndex to enable flexible document querying and semantic retrieval without external vector DBs.
- **Technologies**: Python, LlamaIndex, Google Gemini 1.5 Pro, GeminiEmbedding, dotenv
- **Takeaways**: Local document QA with Gemini is feasible using LlamaIndex’s chunking, embedding, and indexing utilities.

### Project 8 (LLM-Powered RAG with Haystack)

- **Goal**: Build a Retrieval-Augmented Generation (RAG) pipeline using Haystack and OpenAI to answer questions about the Seven Wonders dataset.
- **Key Learnings**: Haystack's component-based API enables modular design with document embedding, retrieval, prompt construction, and LLM-based generation.
- **Technologies**: Python, Haystack, Hugging Face Datasets, SentenceTransformers, OpenAI GPT-3.5-Turbo
- **Takeaways**: Open-domain QA pipelines can be assembled efficiently using Haystack without external databases, leveraging in-memory storage and transformer-based components.

### Project 9 (RAG-Powered PDF QA with Pinecone)

- **Goal**: Enable question answering over a PDF by retrieving semantically relevant text using vector search and generating answers with a language model.
- **Key Learnings**: Retrieval-Augmented Generation improves answer quality by grounding outputs in chunked, embedded source documents processed through a modular pipeline.
- **Technologies**: Python, FastAPI, Pinecone, Haystack, SentenceTransformers, HuggingFace TGI, Uvicorn
- **Takeaways**: Combining document conversion, semantic search, and LLMs in a pipeline makes it easy to build scalable QA systems over custom PDF data.

### Project 10 (Rag with GGemma and VectorMongoDB)
- **Goal**: Generate sentence embeddings from movie plot summaries using a pre-trained transformer model.
- **Key Learnings**: Shows how to clean data and apply NLP embeddings with SentenceTransformers.
- **Technologies**: datasets, pandas, sentence-transformers
- **Takeaways**: Useful pattern for embedding text data for NLP or search applications.

---

## 🔄 Shared Concepts & Reusable Patterns

- [01] Modular pipeline for chunking, embedding, retrieval, and generation
- [02] Use of ensemble retrieval with cross-encoder re-ranking for precision
- [03] Vector comparison using word frequency.
- [04] Text chunking, vector embeddings, similarity search, prompt templating
- [05] Retrieval-Augmented Generation over document chunks using vector embeddings and LLMs.
- [06] Lightweight local RAG using LlamaIndex and HuggingFace-hosted models (no external vector DB required)  
- [07] Modular pipeline for chunking, embedding, retrieval, and generation
- [08] Modular pipeline for chunking, embedding, retrieval, and generation
- [09] The use of Haystack's component-based pipelines (converter → splitter → embedder → retriever → prompt → generator)
- [10] Clean and embed text data using transformer models in a DataFrame pipeline.

---

## Features

- [01] Dynamic, context-aware responses based on live external data
- [02] Support for hybrid retrieval strategies (sparse + dense + structured)
- [03] Streams AI response based on best-matched document.
- [04] FAISS vector index for retrieval
- [05] Seamless integration of Weaviate vector store with HuggingFace for end-to-end document QA.
- [06] Local document loading, embedding, indexing, and querying using LlamaIndex and Mistral LLM  
- [07] Gemini-1.5-Pro-powered document QA over local file-based index
- [08] Dynamic, context-aware responses generated using retrieved documents and OpenAI LLM
- [09] Text indexes it into Pinecone using embeddings, and serves answers using FastAPI and a HTML.
- [10] Adds sentence embeddings to movie plots using MiniLM-L6-v2.
