# RAG-Based Question Answering with LangChain and OpenAI

## Description

This script implements a Retrieval-Augmented Generation (RAG) pipeline using LangChain and OpenAI. It processes a text document, generates vector embeddings, and enables question answering by retrieving relevant context and generating an answer with a language model.

## Usage

1. **Environment Setup**

   Load environment variables from a `.env` file. The script expects:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

2. **Input Data**

   Provide a plain text file named `rowdata.txt` in the same directory. This file will be used to build the knowledge base.

3. **Execution Steps**

   - Load and read the input document.
   - Split the document into overlapping chunks using `RecursiveCharacterTextSplitter`.
   - Embed the text chunks using `OpenAIEmbeddings`.
   - Create a FAISS vector store for similarity search.
   - Build a retriever from the vector store.
   - Define a prompt template for question answering.
   - Use `ChatOpenAI` with the `gpt-4o-mini` model to generate an answer.
   - Invoke the RAG chain on the question:
     ```
     What did the president say about Ketanji Brown Jackson?
     ```

4. **Output**

   The answer to the question is printed to the console. If the retrieved context is insufficient, the response will be:
   ```
   I don't know.
   ```