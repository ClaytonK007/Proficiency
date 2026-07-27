# To-Do list

## Requirements

- allow a task to be added
- toggle a task to mark it as completed
- allow a task to be deleted
(switch branches to V2 for project with PostgreSQL database)

## How to deploy and test:
- download or pull project repository
- create a virtual environment in the repository - run "python -m venv .venv" in your terminal 
- run virtual environment by running "./.venv/Scripts/activate" in your terminal 
- install project requirements - run "pip install -r requirements.txt" in your terminal 
- run server "uvicorn app.main:app --reload" in your terminal
- go to "http://127.0.0.1:8000" or "localhost:8000" in your browser and create a task, toggle it and delete.

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
