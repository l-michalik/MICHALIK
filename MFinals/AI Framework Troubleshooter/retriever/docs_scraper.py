import requests
import re
from typing import List

def scrape_single_page(url: str) -> List[dict]:
    """Fetch and clean visible text content from a single documentation page."""
    try:
        print(f"📄 Fetching: {url}")
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            print(f"❌ Failed to fetch {url}: {response.status_code}")
            return []

        # Basic HTML cleanup
        html = re.sub(r"<script.*?>.*?</script>", "", response.text, flags=re.DOTALL)
        html = re.sub(r"<style.*?>.*?</style>", "", html, flags=re.DOTALL)
        html = re.sub(r"<head.*?>.*?</head>", "", html, flags=re.DOTALL)
        html = re.sub(r"<footer.*?>.*?</footer>", "", html, flags=re.DOTALL)
        html = re.sub(r"<nav.*?>.*?</nav>", "", html, flags=re.DOTALL)

        # Remove all HTML tags
        text = re.sub(r"<[^>]+>", "", html)
        text = re.sub(r"\s+", " ", text).strip()

        if len(text) < 100:
            print(f"⚠️ Skipped (too short): {url}")
            return []

        return [{
            "content": text,
            "source": url
        }]

    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return []
