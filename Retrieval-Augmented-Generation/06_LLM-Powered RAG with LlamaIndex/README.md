# 🦙 RAG with LlamaIndex + Hugging Face

This project demonstrates a simple but powerful **Retrieval-Augmented Generation (RAG)** pipeline using the [LlamaIndex](https://github.com/jerryjliu/llama_index) library with **Mistral 7B Instruct** for LLM inference and **sentence-transformers/all-mpnet-base-v2** for dense retrieval embeddings.

## 📌 What’s in this project?

This implementation covers:

- 🔎 Loading documents from the `./data` directory
- 💬 Using a Hugging Face-hosted **Mistral 7B** model (`mistralai/Mistral-7B-Instruct-v0.1`) for generating answers
- 🔗 Embedding text chunks using `sentence-transformers/all-mpnet-base-v2`
- 🧠 Indexing and querying documents using **LlamaIndex**
- 🛠️ Using `PromptTemplate` to customize system and query formatting

---

## 💡 Why this setup?

| Component | Why it's used |
|----------|----------------|
| `LlamaIndex` | Abstraction over document indexing, chunking, embedding, and querying |
| `HuggingFaceLLM` | Enables direct integration with open-source transformer models via Hugging Face Hub |
| `Mistral 7B Instruct` | Lightweight, instruction-tuned model for accurate and efficient inference |
| `all-mpnet-base-v2` | High-performance embedding model optimized for semantic similarity |
| `.env` + `huggingface_hub.login()` | Keeps Hugging Face API key secure and reusable |
