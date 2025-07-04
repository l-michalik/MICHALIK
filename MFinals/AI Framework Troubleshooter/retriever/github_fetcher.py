from typing import List
import requests

GITHUB_API = "https://api.github.com"

def fetch_repo_files(
    owner: str,
    repo: str,
    max_files: int = 5
) -> List[dict]:
    headers = {"Accept": "application/vnd.github.v3.raw"}
    branch = get_default_branch(owner, repo)
    extensions: List[str] = [".md", ".txt", ".py"]

    results = []

    def fetch_path(path: str):
        if len(results) >= max_files:
            return

        url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}?ref={branch}"
        print(f"🔍 Fetching {url}")
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"❌ Failed to fetch {path}: {response.status_code} — {response.text}")
            return

        data = response.json()

        if isinstance(data, dict) and data.get("type") == "file":
            if any(data["name"].endswith(ext) for ext in extensions):
                content_resp = requests.get(data["download_url"], headers=headers)
                if content_resp.status_code == 200:
                    results.append({
                        "content": content_resp.text,
                        "source": f"{owner}/{repo}/{data['path']}"
                    })

        elif isinstance(data, list):
            for item in data:
                if len(results) >= max_files:
                    break
                if item["type"] == "file" and any(item["name"].endswith(ext) for ext in extensions):
                    content_resp = requests.get(item["download_url"], headers=headers)
                    if content_resp.status_code == 200:
                        results.append({
                            "content": content_resp.text,
                            "source": f"{owner}/{repo}/{item['path']}"
                        })
                elif item["type"] == "dir" and not item["name"].startswith("."):
                    fetch_path(item["path"])  # recurse

    fetch_path("")
    return results


def get_default_branch(owner: str, repo: str) -> str:
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("default_branch", "main")
    else:
        print(f"⚠️ Could not fetch default branch. Using 'main'. Reason: {response.status_code}")
        return "main"
