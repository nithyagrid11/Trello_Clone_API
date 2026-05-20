from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.database import Base

class Board(Base):
    __tablename__ = "boards"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="boards")
    sections = relationship("Section", back_populates="board")
    invitation_token = Column(String(255),nullable=True)
    members = relationship("BoardMember",back_populates="board")