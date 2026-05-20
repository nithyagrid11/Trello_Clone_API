from pydantic import BaseModel
from app.schemas.ticket import TicketSimpleResponse

class SectionBase(BaseModel):
    name: str
    description: str

class SectionCreate(SectionBase):
    board_id: int

class SectionResponse(SectionBase):
    id: int
    board_id: int
    class Config:
        from_attributes = True

class SectionDetailResponse(BaseModel):
    id: int
    name: str
    description: str
    tickets: list[TicketSimpleResponse]
    class Config:
        from_attributes = True