# 🧠 RAG with Cosine Similarity & LLaMA2 (via Ollama)

This project demonstrates a minimal implementation of **Retrieval-Augmented Generation (RAG)** using:
- **Cosine Similarity** for retrieving relevant context.
- **LLaMA2**, served locally via **Ollama**, for generating concise, context-aware responses.

---

## 📚 What is RAG?

**Retrieval-Augmented Generation (RAG)** is a technique that combines:
1. **Retrieval** – Finding relevant documents or context based on a user’s input.
2. **Generation** – Passing that context to a language model to produce a grounded and relevant response.

Instead of relying solely on what the model "knows", RAG provides it with up-to-date, query-specific information at runtime.

---

## 🔍 Document Retrieval: Cosine Similarity

We use a basic form of cosine similarity to compare a user query with a set of candidate documents (called the *corpus*). Here's how it works:

- Each text is treated as a vector of word frequencies.
- The **cosine of the angle** between two such vectors represents their similarity.
- A smaller angle (higher cosine value) means greater similarity.

> 🧪 Example:
> - **User Input:** “I want to relax outdoors”
> - **Corpus:** “Go hiking”, “Watch TV”, “Visit a botanical garden”
> - **Selected Document:** “Visit a botanical garden” (most similar)

---

## 🧠 Response Generation with LLaMA2

Once we retrieve the most relevant document, we construct a structured prompt and pass it to **LLaMA2** running via Ollama. The model is instructed to behave like a short-answer recommendation assistant:

You are a bot that makes recommendations for activities.
You answer in very short sentences and do not include extra information.
This is the recommended activity: {relevant_document}
The user input is: {user_input}
Compile a recommendation to the user based on the recommended activity and the user input.


This format ensures:
- **Concise answers**
- **Grounded recommendations**
- **Minimal hallucination**

---

## 🧪 End-to-End Flow

1. **Input** → User provides a query.
2. **Retrieval** → System calculates cosine similarity with each document.
3. **Selection** → The most similar document is chosen.
4. **Prompting** → A custom prompt is built using the user input + relevant document.
5. **Generation** → The prompt is sent to LLaMA2 via Ollama’s API (`/api/generate`).
6. **Response** → A concise answer is streamed and printed.

---

## 💡 Why This Approach?

This setup is ideal if you want:
- A lightweight RAG prototype
- No dependencies on embedding models or vector databases
- Simple logic using Python and a locally hosted LLM

It is suitable for:
- Activity or product recommendation bots
- FAQ assistants
- Demos or educational tools
- Quick prototyping before scaling up

