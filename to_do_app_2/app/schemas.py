from pydantic import BaseModel, Field
from datetime import datetime

class ToDoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)

class ToDoOut(BaseModel):
    id: int
    title: str
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True