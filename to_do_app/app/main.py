from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from . import models, crud
from .database import engine, SessionLocal, get_db

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")       # Render the list of to-dos
def read_todos(request: Request, page: int = 1, db: Session = Depends(get_db)):
    per_page = 10
    todos, total_pages = crud.get_todos(db, page=page, per_page=per_page)
    return templates.TemplateResponse(
        request,
        "index.html",
        {"todos": todos, "page": page, "total_pages": total_pages},
    )

@app.post("/todos")     # Create a new to-do, then redirect to `/`
def add_todo(title: str = Form(...), db: Session = Depends(get_db)):
    if title.strip():
        crud.create_todo(db, title.strip())
        return RedirectResponse(url="/", status_code=303)
    
@app.post("/todos/{todo_id}/toggle")     # Mark complete/incomplete, then redirect to `/`
def toggle(todo_id: int, db: Session = Depends(get_db)):
    crud.toggle_todo(db, todo_id)
    return RedirectResponse(url="/", status_code=303)

@app.post("/todos/{todo_id}/delete")   # Delete a to-do
def delete(todo_id: int, db: Session = Depends(get_db)):
    crud.delete_todo(db, todo_id)
    return RedirectResponse(url="/", status_code= 303)