from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.database import Base

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    section_id = Column(Integer,ForeignKey("sections.id"))
    assigned_user_id = Column(Integer,ForeignKey("users.id"),nullable=True)
    section = relationship("Section",back_populates="tickets")
    assigned_user = relationship("User",foreign_keys=[assigned_user_id])
    created_by_id = Column(Integer,ForeignKey("users.id"))
    created_by = relationship("User",foreign_keys=[created_by_id])

    