import argparse
from pathlib import Path

from db.weaviate_client import get_weaviate_client, create_schema_if_missing
from db.upsert import upsert_documents
from generator.rag_pipeline import query_index, generate_answer
from retriever.chunker import chunk_text

def cli_index(file_path: str, source: str):
    create_schema_if_missing(get_weaviate_client())

    print(f"📄 Reading file: {file_path}")
    text = Path(file_path).read_text(encoding="utf-8")
    chunks = chunk_text(text)
    docs = [{"content": chunk, "source": source} for chunk in chunks]
    upsert_documents(docs)

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

    query_parser = subparsers.add_parser("query", help="Ask a dev question")
    query_parser.add_argument("--question", required=True, help="Natural language question")

    args = parser.parse_args()

    if args.command == "index":
        cli_index(args.file, args.source)
    elif args.command == "query":
        cli_query(args.question)

if __name__ == "__main__":
    main()
