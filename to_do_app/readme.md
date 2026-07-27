# Full-Stack Python To-Do App: Step-by-Step Guide
### Stack: FastAPI (backend) + SQLite (database) + Jinja2 (templates) + Bootstrap (styling/JS only)

This guide walks through building a complete to-do list web app where **Python does all the logic** (routing, database, business rules) and **JavaScript is used only for Bootstrap's built-in components** (modals, toasts, dismissible alerts) — no custom JS logic, no fetch-based SPA behavior. Every page is rendered server-side by FastAPI + Jinja2.

All code is collected in the **Appendix: Full Code Solutions** at the end. Read through the steps first to understand *why* each piece exists, then copy the code from the appendix.

---

## 1. Architecture Overview

```
Browser (HTML + Bootstrap CSS/JS only)
        │  standard form POST/GET requests
        ▼
FastAPI application (Python)
        │  SQLAlchemy ORM
        ▼
SQLite database (todos.db)
```

- **No JSON API, no fetch() calls.** Every user action (add, complete, delete) is a normal HTML `<form>` submission.
- **FastAPI** handles routing, validation, and talks to the database.
- **Jinja2** renders full HTML pages returned by FastAPI.
- **Bootstrap's JS bundle** is included only so components like modals (e.g., "confirm delete") and dismissible alerts work — you write zero lines of custom JavaScript.

---

## 2. Prerequisites

- Python 3.10+
- Basic familiarity with the command line
- pip installed

Check your Python version before starting:
```
python3 --version
```

---

## 3. Project Structure

Set up the folder layout below before writing any code. Keeping this structure is what lets FastAPI auto-discover templates and static files.

```
todo_app/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI app + routes
│   ├── database.py        # DB engine/session setup
│   ├── models.py           # SQLAlchemy ORM model
│   ├── schemas.py          # Pydantic schemas (validation)
│   └── crud.py             # Database operations
├── templates/
│   ├── base.html            # Shared layout, Bootstrap CDN links
│   └── index.html           # Main to-do list page
├── static/
│   └── custom.css           # Small style tweaks (optional)
├── requirements.txt
└── todos.db                  # Created automatically at runtime
```

Create it with:
```
mkdir -p todo_app/app todo_app/templates todo_app/static
cd todo_app
touch app/__init__.py app/main.py app/database.py app/models.py app/schemas.py app/crud.py
touch templates/base.html templates/index.html static/custom.css requirements.txt
```

---

## 4. Set Up a Virtual Environment and Dependencies

Isolate the project's dependencies so they don't clash with other Python projects on your machine.

```
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

You'll need five packages: `fastapi` (the framework), `uvicorn` (the ASGI server that runs it), `sqlalchemy` (ORM for talking to SQLite), `jinja2` (template engine), and `python-multipart` (required for FastAPI to parse HTML form submissions).

List these in `requirements.txt`, then install with:
```
pip install -r requirements.txt
```

---

## 5. Configure the Database Connection

`app/database.py` is responsible for one thing: creating the SQLAlchemy "engine" (the connection to `todos.db`) and a session factory that the rest of the app borrows from whenever it needs to talk to the database.

Key ideas to understand before writing this file:
- SQLite needs a special connection argument (`check_same_thread=False`) because FastAPI can serve requests from multiple threads.
- `SessionLocal` is a factory — calling it creates a new database session per request.
- `Base` is the declarative base class every ORM model will inherit from.

---

## 6. Define the Data Model

`app/models.py` defines what a "to-do item" looks like as a database table, using SQLAlchemy's ORM.

Each to-do needs:
- `id` — primary key, auto-incrementing
- `title` — the task text (required, indexed for lookups)
- `completed` — boolean flag, defaults to `False`
- `created_at` — timestamp, defaults to the current time

Thinking in terms of columns first makes the next steps (schemas, CRUD) fall into place naturally, since they all mirror this same shape.

---

## 7. Define Pydantic Schemas

`app/schemas.py` defines the shapes of data flowing *into* and *out of* your route functions — separate from the database model. This separation matters: it lets you validate incoming form data independently of how it's stored, and control exactly what's exposed when rendering a page.

You'll define:
- `TodoCreate` — what's required to create a new to-do (just a `title`)
- `TodoOut` — what a to-do looks like once read back (includes `id`, `completed`, `created_at`)

---

## 8. Write the CRUD Functions

`app/crud.py` centralizes every database operation so your route functions in `main.py` stay thin and readable. Each function takes a `Session` object and does exactly one job:

- `get_todos(db)` — return all to-dos, most recent first
- `create_todo(db, title)` — insert a new to-do
- `toggle_todo(db, todo_id)` — flip a to-do's `completed` flag
- `delete_todo(db, todo_id)` — remove a to-do by id

Isolating these functions means if you ever swap SQLite for PostgreSQL, only this file changes — `main.py` doesn't need to know how the data is stored.

---

## 9. Build the FastAPI Routes

`app/main.py` ties everything together. Because JS is Bootstrap-only, **every route returns a full HTML page** rather than JSON — even the "add" and "delete" actions redirect back to the main page after doing their work (the Post/Redirect/Get pattern). This avoids the "resubmit form" browser warning and keeps the whole app working without any client-side scripting.

Routes needed:

| Method | Path                  | Purpose                                      |
|--------|-----------------------|-----------------------------------------------|
| GET    | `/`                   | Render the list of to-dos                     |
| POST   | `/todos`              | Create a new to-do, then redirect to `/`      |
| POST   | `/todos/{id}/toggle`  | Mark complete/incomplete, then redirect to `/`|
| POST   | `/todos/{id}/delete`  | Delete a to-do, then redirect to `/`          |

A dependency function (`get_db`) hands each route a database session and guarantees it's closed afterward, even if an error occurs. FastAPI's `Depends()` mechanism wires this in automatically.

You'll also mount the `/static` folder (for `custom.css`) and configure `Jinja2Templates` pointing at the `templates/` directory.

---

## 10. Build the Templates

**`templates/base.html`** is the shared shell: it pulls in Bootstrap's CSS from a CDN in the `<head>`, and Bootstrap's JS bundle (which powers the delete-confirmation modal) right before `</body>`. This is the *only* JavaScript in the whole project, and you don't write any of it yourself — it's Bootstrap's own bundle.

**`templates/index.html`** extends the base template and contains:
- A Bootstrap form (input + submit button) that POSTs to `/todos` to add a new item
- A Bootstrap list group showing each to-do, with a checkbox (via a small form) to toggle completion
- A delete button per item that triggers a Bootstrap **modal** ("Are you sure?") before the delete form actually submits — this is a stock Bootstrap data-attribute pattern (`data-bs-toggle="modal"`), not custom JS
- Bootstrap styling classes throughout (`list-group`, `form-check`, `btn`, `badge`) for a clean look with zero custom CSS required

---

## 11. Run the App

From the `todo_app/` root, with the virtual environment active:

```
uvicorn app.main:app --reload
```

- `--reload` restarts the server automatically when you edit code — useful during development, remove it in production.
- Visit `http://127.0.0.1:8000` in your browser.
- The first request will auto-create `todos.db` and the `todos` table (handled by a startup step in `main.py`).

---

## 12. Test the Flow

Walk through this checklist manually:

1. Load `/` — you should see an empty list and an "Add" form.
2. Submit a new to-do — the page redirects back to `/` and shows it in the list.
3. Click the checkbox next to a to-do — it should visually strike through / mark as done, and the page reloads via the toggle route.
4. Click delete — a Bootstrap confirmation modal should pop up (JS-powered, but no custom script).
5. Confirm the delete — the item disappears.
6. Restart the server (`Ctrl+C` then re-run `uvicorn`) — data should persist, since it's stored in `todos.db` on disk, not in memory.

---

## 13. Optional Next Steps

- Add due dates or priority levels as new model columns
- Add basic form validation feedback if a title is submitted empty (FastAPI/Pydantic will already reject it — you'd add a friendly Bootstrap alert to show the error instead of a raw 422 response)
- Add pagination if the list grows large
- Swap SQLite for PostgreSQL by changing only the connection string in `database.py`

---

## Appendix: Full Code Solutions

### `requirements.txt`
```
fastapi
uvicorn
sqlalchemy
jinja2
python-multipart
```

### `app/database.py`
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

### `app/models.py`
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

### `app/schemas.py`
```python
from datetime import datetime
from pydantic import BaseModel, Field

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)

class TodoOut(BaseModel):
    id: int
    title: str
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True
```

### `app/crud.py`
```python
from sqlalchemy.orm import Session
from sqlalchemy import desc
from . import models

def get_todos(db: Session):
    return db.query(models.Todo).order_by(desc(models.Todo.created_at)).all()

def create_todo(db: Session, title: str):
    todo = models.Todo(title=title)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def toggle_todo(db: Session, todo_id: int):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo:
        todo.completed = not todo.completed
        db.commit()
    return todo

def delete_todo(db: Session, todo_id: int):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
    return todo
```

### `app/main.py`
```python
from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import models, crud
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_todos(request: Request, db: Session = Depends(get_db)):
    todos = crud.get_todos(db)
    return templates.TemplateResponse(
        "index.html", {"request": request, "todos": todos}
    )

@app.post("/todos")
def add_todo(title: str = Form(...), db: Session = Depends(get_db)):
    if title.strip():
        crud.create_todo(db, title.strip())
    return RedirectResponse(url="/", status_code=303)

@app.post("/todos/{todo_id}/toggle")
def toggle(todo_id: int, db: Session = Depends(get_db)):
    crud.toggle_todo(db, todo_id)
    return RedirectResponse(url="/", status_code=303)

@app.post("/todos/{todo_id}/delete")
def delete(todo_id: int, db: Session = Depends(get_db)):
    crud.delete_todo(db, todo_id)
    return RedirectResponse(url="/", status_code=303)
```

### `templates/base.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}To-Do App{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="/static/custom.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container py-5">
        {% block content %}{% endblock %}
    </div>

    <!-- Bootstrap JS bundle: powers the modal below. No custom JS is written anywhere in this app. -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### `templates/index.html`
```html
{% extends "base.html" %}

{% block title %}My To-Dos{% endblock %}

{% block content %}
<div class="row justify-content-center">
  <div class="col-md-7">
    <h1 class="mb-4 text-center">My To-Do List</h1>

    <form action="/todos" method="post" class="input-group mb-4">
      <input type="text" name="title" class="form-control" placeholder="What needs doing?" required maxlength="200">
      <button class="btn btn-primary" type="submit">Add</button>
    </form>

    {% if todos %}
    <ul class="list-group shadow-sm">
      {% for todo in todos %}
      <li class="list-group-item d-flex justify-content-between align-items-center">
        <form action="/todos/{{ todo.id }}/toggle" method="post" class="form-check d-flex align-items-center mb-0">
          <input class="form-check-input me-2" type="checkbox" onchange="this.form.submit()"
                 {% if todo.completed %}checked{% endif %}>
          <span class="{% if todo.completed %}text-decoration-line-through text-muted{% endif %}">
            {{ todo.title }}
          </span>
        </form>

        <button type="button" class="btn btn-sm btn-outline-danger"
                data-bs-toggle="modal" data-bs-target="#deleteModal{{ todo.id }}">
          Delete
        </button>

        <!-- Bootstrap modal: confirm-before-delete, powered entirely by Bootstrap's own JS bundle -->
        <div class="modal fade" id="deleteModal{{ todo.id }}" tabindex="-1">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">Confirm Delete</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
              </div>
              <div class="modal-body">
                Delete "<strong>{{ todo.title }}</strong>"? This can't be undone.
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <form action="/todos/{{ todo.id }}/delete" method="post" class="mb-0">
                  <button type="submit" class="btn btn-danger">Delete</button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </li>
      {% endfor %}
    </ul>
    {% else %}
    <div class="alert alert-secondary text-center" role="alert">
      No to-dos yet — add one above!
    </div>
    {% endif %}
  </div>
</div>
{% endblock %}
```

### `static/custom.css`
```css
/* Small optional tweaks — Bootstrap handles almost everything */
body {
    min-height: 100vh;
}
```

### `app/__init__.py`
```python
# Intentionally empty — marks app/ as a Python package
```

---

## Quick Start Recap

```
mkdir -p todo_app/app todo_app/templates todo_app/static
cd todo_app
python3 -m venv venv && source venv/bin/activate
# create the files above with the code from the appendix
pip install -r requirements.txt
uvicorn app.main:app --reload
# visit http://127.0.0.1:8000
```