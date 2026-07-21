from sqlalchemy.orm import Session
from sqlalchemy import desc
from . import models 

def get_todos(db: Session):
    return db.query(models.Task).order_by(desc(models.Task.created_at)).all()

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