from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

#   1. Link model to database
Base = declarative_base()

#   2. ORM - map and define object to be used in database.
class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    surname = Column(String(120), unique=True, nullable=False)
    idNo = Column(String(13), unique=True, nullable=False)
    dob = Column(Date, nullable=False)