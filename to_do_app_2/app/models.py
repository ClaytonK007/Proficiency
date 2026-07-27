from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer,primary_key= True, index= True)
    title = Column(String, nullable= False, index= True)
    completed = Column(Boolean, nullable= False, default= False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())