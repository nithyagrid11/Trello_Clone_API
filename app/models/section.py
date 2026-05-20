from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.database import Base

class Section(Base):
    __tablename__ = "sections"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    board_id = Column(Integer, ForeignKey("boards.id"))
    board = relationship("Board", back_populates="sections")
    tickets = relationship("Ticket",back_populates="section")