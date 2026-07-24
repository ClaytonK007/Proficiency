import sqlite3
import requests
import re
from booknames import BOOK_NAMES

DB_PATH = "favourites.db"
BIBLE_SEARCH_URL = "https://bolls.life/v2/find/KJV"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS favourites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reference TEXT NOT NULL,
            text TEXT NOT NULL,
            topic TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def clean_verse_text(raw_html: str) -> str:
    """Strip bolls.life's embedded Strong's numbers, footnotes, and mark/italic tags."""
    text = raw_html
    text = re.sub(r"<S>\d+</S>", "", text)        # remove Strong's number tags entirely
    text = re.sub(r"<sup>.*?</sup>", "", text)     # remove translator footnotes entirely
    text = re.sub(r"</?[^>]+>", "", text)          # strip any remaining tags (e.g. <mark>, <i>)
    text = re.sub(r"\s+", " ", text).strip()       # collapse leftover whitespace
    return text


def search_bible(keyword: str, limit: int = 20):
    params = {
        "search": keyword,
        "match_case": "false",
        "match_whole": "true",
        "limit": limit,
        "page": 1,
    }
    response = requests.get(BIBLE_SEARCH_URL, params=params, timeout=8)
    response.raise_for_status()
    data = response.json()

    results = []
    for verse in data.get("results", []):
        book_name = BOOK_NAMES.get(verse["book"], f"Book {verse['book']}")
        results.append({
            "ref": f"{book_name} {verse['chapter']}:{verse['verse']}",
            "text": clean_verse_text(verse["text"]),
        })
    return results