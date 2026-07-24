from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import requests
import math
from database import *

app = FastAPI()
templates = Jinja2Templates(directory="templates")
init_db()

def get_favourites():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM favourites ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "quotes": [], 
            "keyword": "", 
            "error": None, 
            "status": "", 
            "page": 1, 
            "total_pages": 0
            }
    )

@app.get("/search")
def search(request: Request, keyword: str = "", status: str = "", page: int = 1):
    keyword = keyword.strip()
    quotes = []
    error = None
    total_pages = 0
    limit = 20

    if keyword:
        try:
            quotes, total = search_bible(keyword, limit=limit, page=page)
            total_pages = math.ceil(total / limit) if total else 0
            if not quotes:
                error = f"No verse for '{keyword}'. Please try another topic."
        except requests.RequestException:
            error = "Could not reach the Bible search service right now. Please try again."

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "quotes": quotes, 
            "keyword": keyword,
            "error": error, 
            "status": status,
            "page": page,
            "total_pages": total_pages
            }
    )

@app.post("/favourites/add")
def add_to_favourites(
    reference: str = Form(...),
    text: str = Form(...),
    topic: str = Form(...)
    ):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute(
        "INSERT OR IGNORE INTO favourites (reference, text, topic) VALUES (?, ?, ?)",
        (reference, text, topic)
    )
    conn.commit()
    was_saved = cursor.rowcount > 0
    conn.close()

    status = "saved" if was_saved else "duplicate"
    return RedirectResponse(url=f"/search?keyword={topic}&status={status}", status_code=303)

@app.get("/favourites")
def favourites(request: Request):
    return templates.TemplateResponse(request, "favourites.html", {"favourites": get_favourites()})

@app.post("/favourites/delete/{favourite_id}")
def delete_favourites(request: Request, favourite_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM favourites WHERE id = ?", (favourite_id,))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/favourites", status_code=303)