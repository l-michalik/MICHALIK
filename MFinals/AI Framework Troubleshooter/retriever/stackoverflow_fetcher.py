import requests
import time
from typing import List


def fetch_stackoverflow_answers(query: str, max_questions: int = 1) -> List[dict]:
    print(f"🔍 Searching Stack Overflow for: {query}")
    search_url = "https://api.stackexchange.com/2.3/search/advanced"
    answer_url = "https://api.stackexchange.com/2.3/questions/{ids}/answers"

    params = {
        "order": "desc",
        "sort": "relevance",
        "q": query,
        "site": "stackoverflow",
        "accepted": "True",
        "filter": "default",
        "pagesize": max_questions,
    }

    try:
        search_resp = requests.get(search_url, params=params)
        search_resp.raise_for_status()
        questions = search_resp.json().get("items", [])

        if not questions:
            print("⚠️ No matching questions found.")
            return []

        question_ids = [str(q["question_id"]) for q in questions]
        ids_str = ";".join(question_ids)

        ans_params = {
            "order": "desc",
            "sort": "votes",
            "site": "stackoverflow",
            "filter": "withbody",
        }

        answer_resp = requests.get(answer_url.format(ids=ids_str), params=ans_params)
        answer_resp.raise_for_status()
        answers = answer_resp.json().get("items", [])

        results = []
        for q in questions:
            results.append({
                "content": strip_html_tags(q["title"]),
                "source": q["link"]
            })

        for a in answers:
            results.append({
                "content": strip_html_tags(a["body"]),
                "source": f"https://stackoverflow.com/a/{a['answer_id']}"
            })

        return results

    except Exception as e:
        print(f"❌ Stack Overflow fetch failed: {e}")
        return []


def strip_html_tags(html: str) -> str:
    import re
    text = re.sub(r"<[^>]+>", "", html)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
