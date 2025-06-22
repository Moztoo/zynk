import json
from pathlib import Path
import requests
import feedparser
from .utils import extract_content

def load_feeds_json(path="feeds.json"):
    file = Path(path)
    if not file.exists():
        raise FileNotFoundError(f"Feed file '{path}' not found.")
    with file.open("r", encoding="utf-8") as f:
        return json.load(f)

def fetch_articles(feeds, timeout=5):
    articles = []
    for source_name, url in feeds.items():
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            feed = feedparser.parse(response.content)
            for entry in feed.entries:
                articles.append({
                "title": entry.title,
                "summary": extract_content(entry),
                "link": entry.link,
                "source": source_name,
                "published": entry.get("published")  # puede ser None
            })
        except Exception as e:
            print(f"Skipping {source_name}: {e}")
    return articles
