# ✨ AI Framework Troubleshooter

## 🚩 Problem

Modern developers working with fast-evolving AI/ML frameworks like LangChain, HuggingFace Transformers, FastAPI, and others often face a major pain point: finding reliable, up-to-date information when things go wrong.

Despite the abundance of available documentation and community forums, information is scattered and often outdated, incomplete, or buried deep within GitHub issues, changelogs, Stack Overflow threads, and blog posts. Developers frequently encounter situations like:

- A function or class is deprecated with no mention in the main docs.
- An error message appears without context, and Stack Overflow has conflicting answers.
- A library update silently changes behavior, breaking previously working code.
- Examples in tutorials don't reflect current best practices or latest APIs.

This leads to a frustrating, time-consuming cycle of searching, skimming, and guessing — especially under time pressure or in production environments.

**The core problem:** There is no single source of truth that can synthesize and contextualize scattered documentation and community knowledge for a specific developer question.

**Goal of this project:** To solve that by using Retrieval-Augmented Generation (RAG) to provide developers with relevant, context-aware, and up-to-date answers — grounded in actual source content from documentation, GitHub repos, and forums.

## 🚀 Features

### 1. 🔍 Multi-source Semantic Retrieval
Retrieve relevant content from:
- Official documentation (e.g., LangChain, Transformers)
- GitHub files (e.g., README.md, changelogs, examples)
- Stack Overflow answers and questions  
Using vector embeddings + similarity search Weawiate.

---

### 2. 🧠 Context-Aware Answer Generation (RAG Core)
Inject retrieved content into an LLM prompt to:
- Provide grounded, source-aware answers
- Format responses for developers (e.g., with code blocks)
- Avoid hallucination by constraining to retrieved context

---

### 3. 🔁 Automatic Index Refresh
Regularly update vector indexes by re-fetching source data:
- GitHub API clones or direct scraping
- Stack Overflow API based on specific tags
- Documentation auto-refresh pipelines

---

### 4. 🧾 Source Attribution & Traceability
Each answer includes:
- Snippets of the original content
- Source links for validation
- Inline citations where applicable

---

### 5. 🧪 Version-Aware Question Routing (Optional)
Route queries to the correct framework version by detecting:
- Version mentions in user queries (e.g., "LangChain 0.1.6")
- Changelog-aware context inclusion


## 📂 Folder Structure

```
ai-framework-troubleshooter/
├── data/
│   └── processed/               # Cleaned & chunked docs (stored)
│
├── db/
│   ├── weaviate_client.py       # Handles cloud vector index operations
│   ├── schema.py                # Weaviate class/schema definitions
│   └── upsert.py                # Pushes documents to Weaviate
│
├── retriever/
│   ├── github_fetcher.py
│   ├── docs_scraper.py
│   ├── stackoverflow_fetcher.py
│   ├── chunker.py
│   └── embedder.py              # Sends embeddings to Weaviate
│
├── generator/
│   ├── prompt_template.py
│   ├── llm_runner.py            # Calls Hugging Face LLM
│   └── rag_pipeline.py          # Full RAG logic using cloud index + LLM
│
├── app/
│   └── api.py                   # FastAPI endpoint to serve answers
│
├── utils/
│   ├── config.py                # Load API keys, endpoints from env
│   └── logging_config.py
│
├── tests/
│   ├── test_vector_db.py
│   ├── test_retrieval.py
│   └── test_pipeline.py
│
├── main.py                      # CLI tool (e.g., query, embed, update)
├── pyproject.toml
├── .env
└── README.md
```


## 🛠 Setup

This project uses [`uv`](https://github.com/astral-sh/uv) — a superfast Python package manager — for dependency management.

### 4. Set up environment variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_key
```

## 🧪 Usage

Once your environment is set up, you can start querying the assistant:

```bash
uv run main.py query --question "Why is load_chain not working?"
uv run main.py index --file docs/langchain.md --source "LangChain Docs"
uv run main.py index-github --owner langchain-ai --repo langchain
uv run main.py index-stack --question "how to load pdfs in langchain"
```

Version-aware query routing
Deployment and hosting
Documentation and usage examples