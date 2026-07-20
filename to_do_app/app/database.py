from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./to_do_app.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_threads": False})
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()