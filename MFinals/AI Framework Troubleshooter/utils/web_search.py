from serpapi import GoogleSearch # type: ignore
from utils.config import Config

def search_docs_for_question(question: str) -> str | None:
    query = f"{question}"
    print(f"🔎 Searching via SerpAPI: {query}")

    try:
        search = GoogleSearch({
            "q": query,
            "api_key": Config.SERPAPI_API_KEY,
            "num": 10
        })
        results = search.get_dict()

        for result in results.get("organic_results", []):
            link = result.get("link")
            if link and is_documentation_link(link):
                print(f"🔗 Found: {link}")
                return link

    except Exception as e:
        print(f"❌ SerpAPI search failed: {e}")

    return None

from urllib.parse import urlparse
def is_documentation_link(url: str) -> bool:
    parsed = urlparse(url)
    return (
        parsed.scheme in {"http", "https"}
        and parsed.netloc
        and not parsed.netloc.startswith("www.google")
        and len(parsed.path.strip("/")) > 0
    )
