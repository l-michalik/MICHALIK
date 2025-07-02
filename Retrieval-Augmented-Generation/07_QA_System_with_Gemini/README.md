# 🧠 LLM-Powered RAG with Gemini & LlamaIndex

This project demonstrates how to build a lightweight Retrieval-Augmented Generation (RAG) system using **Google Gemini 1.5 Pro** and **LlamaIndex**. It enables local document question-answering (QA) by embedding and indexing text files from a local directory.

---

## 📌 What This Project Does

- Loads documents from the `../data` folder
- Splits large documents into smaller chunks to comply with model limits
- Embeds the text using **GeminiEmbedding**
- Creates a persistent **VectorStoreIndex** for semantic retrieval
- Uses **Gemini 1.5 Pro** for answering natural language questions based on the indexed content
