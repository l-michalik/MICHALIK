import argparse
from pathlib import Path

from db.weaviate_client import get_weaviate_client, create_schema_if_missing
from db.upsert import upsert_documents
from generator.rag_pipeline import query_index, generate_answer
from retriever.chunker import chunk_text
from retriever.github_fetcher import fetch_repo_files
from utils.web_search import search_docs_for_question
from retriever.docs_scraper import scrape_single_page
from retriever.stackoverflow_fetcher import fetch_stackoverflow_answers

def cli_stackoverflow(question: str):
    print(f"📦 Fetching Stack Overflow results for: {question}")
    results = fetch_stackoverflow_answers(question)

    if not results:
        print("⚠️ No Stack Overflow results found.")
        return

    all_chunks = []
    for doc in results:
        for chunk in chunk_text(doc["content"]):
            all_chunks.append({
                "content": chunk,
                "source": doc["source"]
            })

    print(f"📤 Upserting {len(all_chunks)} chunks from Stack Overflow...")
    upsert_documents(all_chunks)

    print("✅ Done. You can now rerun your query with updated context.")

def cli_index(file_path: str, source: str):

    print(f"📄 Reading file: {file_path}")
    text = Path(file_path).read_text(encoding="utf-8")
    chunks = chunk_text(text)
    docs = [{"content": chunk, "source": source} for chunk in chunks]
    upsert_documents(docs)

def cli_index_github(owner: str, repo: str):

    print(f"📦 Fetching up to 5 files from GitHub repo: {owner}/{repo}")
    files = fetch_repo_files(owner=owner, repo=repo, max_files=5)

    all_chunks = []
    for file in files:
        chunks = chunk_text(file["content"])
        for chunk in chunks:
            doc = {
                "content": chunk,
                "source": file["source"]
            }
            all_chunks.append(doc)

    print(f"📤 Upserting {len(all_chunks)} chunks to vector DB...")
    upsert_documents(all_chunks)

def cli_query(question: str):
    chunks = query_index(question)
    
    if not chunks:
        print("⚠️ No relevant context found. Searching for docs...")

        doc_url = search_docs_for_question(question)
        if not doc_url:
            print("❌ Could not find any documentation link.")
            return

        scraped = scrape_single_page(doc_url)
        if not scraped:
            print("❌ Failed to scrape or extract content.")
            return

        docs = []
        for doc in scraped:
            for chunk in chunk_text(doc["content"]):
                docs.append({
                    "content": chunk,
                    "source": doc["source"]
                })

        print(f"📥 Indexing {len(docs)} new chunks...")
        upsert_documents(docs)

        chunks = query_index(question)
        if not chunks:
            print("❌ Still no context found after indexing.")
            return

    answer = generate_answer(question, chunks)
    print(answer)

def main():
    create_schema_if_missing(get_weaviate_client())
    parser = argparse.ArgumentParser(description="🧠 AI Framework Troubleshooter CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    index_parser = subparsers.add_parser("index", help="Index a markdown/text file into Weaviate")
    index_parser.add_argument("--file", required=True, help="Path to file (.md or .txt)")
    index_parser.add_argument("--source", required=True, help="Source label (e.g., 'LangChain Docs')")

    github_parser = subparsers.add_parser("index-github", help="Index GitHub content into Weaviate")
    github_parser.add_argument("--owner", required=True, help="GitHub org/user name")
    github_parser.add_argument("--repo", required=True, help="GitHub repository name")

    query_parser = subparsers.add_parser("query", help="Ask a dev question")
    query_parser.add_argument("--question", required=True, help="Natural language question")
    query_parser.add_argument("--owner", help="GitHub org/user (for fallback indexing)")
    query_parser.add_argument("--repo", help="GitHub repo name (for fallback indexing)")
    
    stack_parser = subparsers.add_parser("index-stack", help="Fetch and index Stack Overflow answers")
    stack_parser.add_argument("--question", required=True, help="Natural language dev question")

    args = parser.parse_args()

    if args.command == "index":
        cli_index(args.file, args.source)
    elif args.command == "index-github":
        cli_index_github(args.owner, args.repo)
    elif args.command == "query":
        cli_query(args.question, owner=args.owner, repo=args.repo)
    elif args.command == "index-stack":
        cli_stackoverflow(args.question)


if __name__ == "__main__":
    main()
