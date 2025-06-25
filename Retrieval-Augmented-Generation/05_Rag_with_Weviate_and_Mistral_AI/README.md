# RAG-Powered PDF QA with Weaviate and HuggingFace

## Description

This script implements a Retrieval-Augmented Generation (RAG) pipeline using LangChain, HuggingFace, and Weaviate to enable question answering over the contents of a PDF file. It loads and processes a PDF, splits it into text chunks, embeds them using a transformer model, stores them in a Weaviate vector database, and allows querying by embedding the question and retrieving the most relevant chunks for answer generation.

## Functionality

- **PDF Ingestion:** Loads a PDF file (`rag.pdf`) and extracts its content (with image extraction).
- **Text Splitting:** Splits the extracted content into overlapping text chunks.
- **Embedding Generation:** Uses HuggingFace model `sentence-transformers/all-mpnet-base-v2` to embed the text chunks.
- **Weaviate Storage:** Uploads the text chunks and their embeddings into a Weaviate cloud collection (`rag_knowledge_base`).
- **Query Embedding and Retrieval:** Embeds a query string (e.g., `"What is rag?"`) and retrieves the top 3 similar chunks using vector search.
- **Answer Generation:** Combines the retrieved chunks as context and uses `mistralai/Mistral-7B-Instruct-v0.2` from HuggingFaceHub to generate an answer.
