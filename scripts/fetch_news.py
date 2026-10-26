"""Fetch recent articles from public RSS feeds."""
import calendar
import datetime as dt
import email.utils
import feedparser
import requests

FEEDS = {
    "tech": [
        "https://feeds.bbci.co.uk/news/technology/rss.xml",
        "https://www.theverge.com/rss/index.xml",
    ],
    "world": [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://www.theguardian.com/world/rss",
    ],
}

def fetch(max_age_hours=48):
    now = dt.datetime.now(dt.timezone.utc)
    items = []
    for category, urls in FEEDS.items():
        for url in urls:
            try:
                response = requests.get(url, timeout=20, headers={"User-Agent": "daily-news/1.0"})
                response.raise_for_status()
                parsed = feedparser.parse(response.content)
                for entry in parsed.entries[:35]:
                    stamp = entry.get("published_parsed") or entry.get("updated_parsed")
                    if not stamp:
                        continue
                    published = dt.datetime.fromtimestamp(calendar.timegm(stamp), dt.timezone.utc)
                    if not dt.timedelta(0) <= now - published <= dt.timedelta(hours=max_age_hours):
                        continue
                    link = entry.get("link", "")
                    if not link.startswith("https://"):
                        continue
                    items.append({"category": category, "title": entry.get("title", ""),
                                  "summary": entry.get("summary", "")[:1200],
                                  "url": link, "published": published.isoformat(),
                                  "source": parsed.feed.get("title", url)})
            except (requests.RequestException, ValueError) as exc:
                print(f"Feed unavailable: {url}: {exc}")
    return sorted({x["url"]: x for x in items}.values(),
                  key=lambda x: x["published"], reverse=True)

if __name__ == "__main__":
    import json
    print(json.dumps(fetch(), ensure_ascii=False, indent=2))
