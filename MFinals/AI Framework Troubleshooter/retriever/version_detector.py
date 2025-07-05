import re

def detect_version(text: str) -> str | None:
    """Extracts version like '0.1.6' or 'v4.39.2' from a string."""
    match = re.search(r"\bv?(\d+\.\d+(?:\.\d+)?)\b", text)
    return match.group(1) if match else None
