from sqlalchemy.orm import Session
from sqlalchemy import desc
from . import models

def get_todos(db: Session, page: int = 1, per_page: int = 10):
    offset = (page - 1) * per_page
    total = db.query(models.Task).count()
    todos = (
        db.query(models.Task)
        .order_by(desc(models.Task.created_at))
        .offset(offset)
        .limit(per_page)
        .all()
    )
    total_pages = max(1, (total + per_page - 1) // per_page)  # ceiling division
    return todos, total_pages

def create_todo(db: Session, title: str):
    todo = models.Task(title= title)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def toggle_todo(db: Session, todo_id: int):
    todo = db.query(models.Task).filter(models.Task.id == todo_id).first()
    if todo:
        todo.completed = not todo.completed
        db.commit()
    return todo

def delete_todo(db: Session, todo_id: int):
    todo = db.query(models.Task).filter(models.Task.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
    return todo