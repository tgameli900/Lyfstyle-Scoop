"""
scrapers.py - Region-Balanced News Scraper & Aggregator.

Fetches the latest articles across Ghana, Nigeria, USA, UK, Canada & West Africa,
filters for freshness (past X hours), deduplicates headlines, and ensures a balanced
selection representing both regional Afrobeats/Ghana updates and major global scoops.
"""

import time
import datetime
import re
from bs4 import BeautifulSoup
import feedparser
import requests
from config import ENTERTAINMENT_RSS_FEEDS, HOURS_WINDOW, MAX_STORIES_PER_DIGEST


def clean_html(raw_html: str) -> str:
    """Removes HTML tags, extra whitespace, and image links from text."""
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text(separator=" ")
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:800]


def fetch_feed_articles(feed_info: dict, cutoff_time: float) -> list:
    """Fetches articles from a single RSS feed published after cutoff_time."""
    articles = []
    feed_url = feed_info["url"]
    feed_name = feed_info["name"]
    feed_region = feed_info["region"]

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        resp = requests.get(feed_url, headers=headers, timeout=10)
        if resp.status_code != 200:
            return articles

        parsed_feed = feedparser.parse(resp.content)

        for entry in parsed_feed.entries:
            pub_time = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                pub_time = time.mktime(entry.published_parsed)
            elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                pub_time = time.mktime(entry.updated_parsed)
            else:
                pub_time = time.time() - 3600

            if pub_time >= cutoff_time:
                title = entry.get("title", "").strip()
                url = entry.get("link", "").strip()
                
                summary_raw = entry.get("summary", "")
                if hasattr(entry, "content") and entry.content:
                    summary_raw = entry.content[0].get("value", summary_raw)
                
                summary = clean_html(summary_raw)

                # Clean up " - Source Name" suffix commonly found in Google News titles
                if " - " in title and "Google News" in feed_name:
                    parts = title.rsplit(" - ", 1)
                    if len(parts) == 2 and len(parts[1]) < 30:
                        title = parts[0].strip()

                if title and url and len(title) > 10:
                    articles.append({
                        "title": title,
                        "url": url,
                        "source": feed_name,
                        "region": feed_region,
                        "category": feed_info.get("category", "Pop Culture"),
                        "summary": summary,
                        "pub_time": pub_time,
                        "published": datetime.datetime.fromtimestamp(pub_time).strftime("%Y-%m-%d %H:%M:%S")
                    })
    except Exception as e:
        pass

    return articles


def get_top_entertainment_news(max_stories: int = MAX_STORIES_PER_DIGEST, hours_window: int = HOURS_WINDOW) -> list:
    """
    Scours regional and global entertainment feeds, deduplicates by title similarity,
    and returns a region-balanced selection of the hottest `max_stories` articles.
    """
    print(f"[*] Scouring entertainment news across {len(ENTERTAINMENT_RSS_FEEDS)} publications (Last {hours_window} hrs)...")
    cutoff_time = time.time() - (hours_window * 3600)
    all_articles = []

    for feed_info in ENTERTAINMENT_RSS_FEEDS:
        print(f"    -> Checking [{feed_info['region']}] {feed_info['name']}...")
        feed_articles = fetch_feed_articles(feed_info, cutoff_time)
        all_articles.extend(feed_articles)

    print(f"[*] Total recent articles found across all regions: {len(all_articles)}")

    # Deduplicate articles based on normalized title similarity
    unique_articles = []
    seen_titles = set()

    all_articles.sort(key=lambda x: x["pub_time"], reverse=True)

    for art in all_articles:
        norm_title = re.sub(r'[^a-zA-Z0-9]', '', art["title"].lower())[:35]
        if norm_title not in seen_titles and len(norm_title) > 8:
            seen_titles.add(norm_title)
            unique_articles.append(art)

    # Group deduplicated articles by Region
    by_region = {
        "Ghana & West Africa": [],
        "Nigeria & Afrobeats": [],
        "USA & Global": [],
        "United Kingdom": [],
        "Canada": []
    }

    for art in unique_articles:
        reg = art.get("region", "USA & Global")
        if reg in by_region:
            by_region[reg].append(art)
        else:
            by_region["USA & Global"].append(art)

    print("\n[*] Breakdown of unique recent stories by region:")
    for reg, items in by_region.items():
        print(f"    • {reg}: {len(items)} stories available")

    # Region-Balanced Selection Strategy:
    # We pick stories in round-robin fashion starting with Ghana/West Africa, Nigeria, USA, UK, Canada
    # until max_stories is reached!
    selected = []
    priority_order = [
        "Ghana & West Africa",
        "Nigeria & Afrobeats",
        "USA & Global",
        "United Kingdom",
        "Canada"
    ]

    # Pass 1: Try to get at least 1 story from every region that has news
    for reg in priority_order:
        if len(selected) >= max_stories:
            break
        if by_region[reg]:
            selected.append(by_region[reg].pop(0))

    # Pass 2: If more slots available, add more from Ghana, Nigeria, USA in rotation
    while len(selected) < max_stories and any(by_region.values()):
        for reg in priority_order:
            if len(selected) >= max_stories:
                break
            if by_region[reg]:
                selected.append(by_region[reg].pop(0))

    print(f"\n[*] Selected {len(selected)} top stories balanced across your focus regions.")
    return selected
