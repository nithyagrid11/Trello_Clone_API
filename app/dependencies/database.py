#this file manages the db session lifecycle per request, ensuring that connections are properly opened and closed.
from app.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()