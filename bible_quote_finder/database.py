import sqlite3

DB_PATH = "favourites.db"
BIBLE_SEARCH_URL = "https://judeasoftware.com/api/kjv/search.php"

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