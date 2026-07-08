#!/usr/bin/env python3
"""
Holt die neusten Artikel vom WNTI-RSS-Feed und schreibt sie in posts.json.
Läuft automatisch via GitHub Action (siehe .github/workflows/update-feed.yml).
Benötigt nur die Python-Standardbibliothek.
"""
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

FEED_URL = "https://wnti.ch/api/rss-feed"
OUTPUT = "posts.json"
MAX_POSTS = 4
UA = {"User-Agent": "Mozilla/5.0 (compatible; wnti-linkinbio/1.0)"}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def text(el, *tags):
    """Ersten nicht-leeren Text der angegebenen Tags zurückgeben (namespace-tolerant)."""
    if el is None:
        return None
    for tag in tags:
        for child in el.iter():
            local = child.tag.split('}')[-1]
            if local == tag and child.text and child.text.strip():
                return child.text.strip()
    return None


def find_image_in_item(item):
    """Bild direkt aus dem RSS-Item ziehen (enclosure, media:content, media:thumbnail)."""
    for child in item.iter():
        local = child.tag.split('}')[-1]
        if local in ("enclosure", "content", "thumbnail"):
            url = child.get("url")
            if url and re.search(r"(image|jpe?g|png|webp)", (child.get("type") or "") + url, re.I):
                return url
    # Bild im description/content-HTML?
    html = text(item, "encoded") or text(item, "description") or ""
    m = re.search(r'<img[^>]+src="([^"]+)"', html)
    return m.group(1) if m else None


def og_image(article_url):
    """Fallback: og:image von der Artikelseite lesen."""
    try:
        html = fetch(article_url).decode("utf-8", errors="ignore")
        m = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', html) or \
            re.search(r'<meta[^>]+content="([^"]+)"[^>]+property="og:image"', html)
        return m.group(1).replace("&amp;", "&") if m else None
    except Exception as e:
        print(f"  og:image fehlgeschlagen für {article_url}: {e}", file=sys.stderr)
        return None


def parse_date(raw):
    if not raw:
        return None
    try:
        return parsedate_to_datetime(raw).isoformat()
    except Exception:
        return raw  # ISO-Format o.ä. direkt durchreichen


def main():
    xml_data = fetch(FEED_URL)
    root = ET.fromstring(xml_data)

    items = [el for el in root.iter() if el.tag.split('}')[-1] == "item"]
    if not items:
        # Atom-Feeds nutzen <entry>
        items = [el for el in root.iter() if el.tag.split('}')[-1] == "entry"]

    posts = []
    for item in items[:MAX_POSTS]:
        title = text(item, "title")
        link = text(item, "link", "guid")
        if link is None:  # Atom: <link href="...">
            for child in item.iter():
                if child.tag.split('}')[-1] == "link" and child.get("href"):
                    link = child.get("href")
                    break
        if not title or not link:
            continue
        date = parse_date(text(item, "pubDate", "published", "updated", "date"))
        image = find_image_in_item(item) or og_image(link)
        posts.append({"title": title, "link": link, "date": date, "image": image})
        print(f"OK: {title}")

    if not posts:
        print("FEHLER: Keine Artikel im Feed gefunden – posts.json bleibt unverändert.", file=sys.stderr)
        sys.exit(1)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump({"updated": True, "posts": posts}, f, ensure_ascii=False, indent=2)
    print(f"{len(posts)} Artikel nach {OUTPUT} geschrieben.")


if __name__ == "__main__":
    main()
