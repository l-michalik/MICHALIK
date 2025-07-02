# Seven Wonders RAG Pipeline with Haystack

This project demonstrates a basic Retrieval-Augmented Generation (RAG) pipeline using the [Haystack](https://haystack.deepset.ai/) framework. It embeds documents, retrieves relevant context based on a user question, and generates an answer using OpenAI's GPT model.

## Description

The pipeline uses a dataset about the Seven Wonders of the Ancient World and builds a question-answering system based on it. It follows these steps:

- Loads documents from the `"bilgeyucel/seven-wonders"` dataset via Hugging Face `datasets`
- Embeds documents using `sentence-transformers/all-MiniLM-L6-v2`
- Writes embedded documents into an in-memory document store
- Takes a natural language question as input
- Embeds the question and retrieves relevant documents
- Builds a prompt using a simple Jinja-style template
- Sends the prompt to OpenAI's GPT-3.5-Turbo model and prints the answer