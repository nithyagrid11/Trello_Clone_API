from fastapi import FastAPI
from app.database import Base, engine
from app.models import User
from app.routes.auth import router as auth_router
from app.schemas.user import Token
from app.routes import users
from app.routes import boards
from app.routes import sections
from app.routes import tickets
from app.models.board_member import BoardMember

app = FastAPI()

# Create any missing tables when the server starts.
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

