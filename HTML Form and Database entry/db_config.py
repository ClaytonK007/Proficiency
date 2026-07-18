from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#   1. Create db address variable with the database connection
DATABASE_URL = "sqlite:///./app.db"

#   2. Create engine variable to bridge code with database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

#   3. Create a session to manage transactions between database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#   4. Dependency to provide database sessions to endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()