# RAG-Powered PDF QA System with Haystack and Pinecone

This project implements an end-to-end Retrieval-Augmented Generation (RAG) pipeline using the Haystack framework. It allows users to ask questions about the content of a PDF document via a web interface built with FastAPI. The system retrieves semantically relevant text chunks from the PDF using vector search (Pinecone), and generates an answer using a language model hosted via Hugging Face Text Generation Inference (TGI).

---

## 📌 Features

- PDF document ingestion and indexing using Haystack pipelines
- Sentence-level document splitting and embedding with SentenceTransformers
- Vector-based retrieval using Pinecone
- Prompt-based answer generation using Hugging Face TGI (Mistral model)
- Interactive web UI with FastAPI and Jinja2 templates

---

## 🚀 How It Works

1. **Ingestion Pipeline**
   - PDF is loaded using `PyPDFToDocument`.
   - The content is split into short chunks using `DocumentSplitter`.
   - Each chunk is embedded using `SentenceTransformersDocumentEmbedder`.
   - Embeddings are stored in Pinecone via `DocumentWriter`.

2. **Query Pipeline**
   - User question is embedded using `SentenceTransformersTextEmbedder`.
   - `PineconeEmbeddingRetriever` searches for relevant chunks.
   - A prompt is dynamically built using `PromptBuilder`.
   - `HuggingFaceTGIGenerator` uses the prompt and generates the answer.

3. **Web Interface**
   - Users interact through a simple form rendered from `index.html`.
   - Submitted queries are processed by a FastAPI route (`/get_answer`).
   - Answers are returned as JSON and displayed to the user.