from sqlalchemy import Column, Integer, String
from .database import Base

class Favourites(Base):

    __tablename__ = "favourites"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    reference = Column(String, nullable=False, unique=True)