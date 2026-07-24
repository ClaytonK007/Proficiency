from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import requests
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
        {"quotes": [], "favourites": get_favourites(), "keyword": "", "error": None})

@app.get("/search")
def search(request: Request, keyword: str = ""):
    keyword = keyword.strip()
    quotes = []
    error = None

    if keyword:
        try:
            quotes = search_bible(keyword, limit=20)
            if not quotes:
                error = f"No verse for '{keyword}'. Please try another topic."
        except requests.RequestException:
            error = "Could not reach the Bible search service right now. Please try again."

    return templates.TemplateResponse(
        request,
        "index.html",
        {"quotes": quotes, "favourites": get_favourites(), "keyword": keyword, "error": error}
    )

@app.post("/favourites/add")
def add_to_favourites(
    reference: str = Form(...),
    text: str = Form(...),
    topic: str = Form(...)
    ):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO favourites (reference, text, topic) VALUES (?, ?, ?)",
        (reference, text, topic)
    )
    conn.commit()
    conn.close()
    return RedirectResponse(url=f"/search?keyword={topic}", status_code=303)

@app.get("/favourites")
def favourites(request: Request):
    return templates.TemplateResponse(request, "favourites.html", {"favourites": get_favourites()})

@app.post("/favourites/delete/{favourite_id}")
def delete_favourites(request: Request, favourite_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM favourites WHERE id = ?", (favourite_id,))
    conn.commit()
    conn.close()
    
    return templates.TemplateResponse(request, "favourites.html", {"favourites": get_favourites()})

