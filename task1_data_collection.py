import requests
import json
import os
import time
from datetime import datetime

headers = {"User-Agent": "TrendPulse/1.0"}

categories = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

def get_category(title):
    title = title.lower()
    for category, words in categories.items():
        for word in words:
            if word.lower() in title:
                return category
    return None

try:
    response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", headers=headers, timeout=10)
    response.raise_for_status()
    story_ids = response.json()[:500]
except requests.RequestException as e:
    print("Failed to fetch top stories:", e)
    story_ids = []

result = []
counts = {
    "technology": 0,
    "worldnews": 0,
    "sports": 0,
    "science": 0,
    "entertainment": 0
}

used_ids = set()
collected_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for category in categories:
    for story_id in story_ids:
        if counts[category] >= 25:
            break

        if story_id in used_ids:
            continue

        try:
            r = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json", headers=headers, timeout=10)
            r.raise_for_status()
            story = r.json()
        except requests.RequestException as e:
            print(f"Failed to fetch story {story_id}: {e}")
            continue

        if not story or "title" not in story:
            continue

        matched_category = get_category(story["title"])

        if matched_category == category:
            result.append({
                "post_id": story.get("id"),
                "title": story.get("title"),
                "category": category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", ""),
                "collected_at": collected_at
            })
            counts[category] += 1
            used_ids.add(story_id)

    time.sleep(2)

os.makedirs("data", exist_ok=True)
filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

with open(filename, "w", encoding="utf-8") as file:
    json.dump(result, file, indent=4)

print(f"Collected {len(result)} stories. Saved to {filename}")