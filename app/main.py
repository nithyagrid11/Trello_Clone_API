from fastapi import FastAPI
from app.database import Base, engine
import os
from app.models import User
from app.routes.auth import router as auth_router
from app.schemas.user import Token
from app.routes import users
from app.routes import boards
from app.routes import sections
from app.routes import tickets
from app.models.board_member import BoardMember

app = FastAPI()

# Create tables only when explicitly requested (avoid connecting at import time).
# Set environment variable CREATE_TABLES=1 to enable automatic table creation on startup.
if os.getenv("CREATE_TABLES", "0") == "1":
    @app.on_event("startup")
    def startup_create_tables():
        Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(users.router)
app.include_router(boards.router)
app.include_router(sections.router)
app.include_router(tickets.router)

@app.get("/")
def root():
    return {"message": "API running successfully"}

