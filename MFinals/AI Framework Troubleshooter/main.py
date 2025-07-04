import argparse
from pathlib import Path

from db.weaviate_client import get_weaviate_client, create_schema_if_missing
from db.upsert import upsert_documents
from generator.rag_pipeline import query_index, generate_answer
from retriever.chunker import chunk_text
from retriever.github_fetcher import fetch_repo_files

def cli_index(file_path: str, source: str):
    create_schema_if_missing(get_weaviate_client())

    print(f"📄 Reading file: {file_path}")
    text = Path(file_path).read_text(encoding="utf-8")
    chunks = chunk_text(text)
    docs = [{"content": chunk, "source": source} for chunk in chunks]
    upsert_documents(docs)

def cli_index_github(owner: str, repo: str):
    create_schema_if_missing(get_weaviate_client())

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
    answer = generate_answer(question, chunks)
    print(answer)

def main():
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

    args = parser.parse_args()

    if args.command == "index":
        cli_index(args.file, args.source)
    elif args.command == "index-github":
        cli_index_github(args.owner, args.repo)
    elif args.command == "query":
        cli_query(args.question)

if __name__ == "__main__":
    main()
