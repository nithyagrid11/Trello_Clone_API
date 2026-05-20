from pydantic import BaseModel

class TicketBase(BaseModel):
    name: str
    description: str

class TicketCreate(TicketBase):
    section_id: int
    assigned_user_id: int | None = None

class TicketResponse(TicketBase):
    id: int
    section_id: int
    assigned_user_id: int | None
    created_by_id: int
    class Config:
        from_attributes = True

class TicketSimpleResponse(BaseModel):
    id: int
    name: str
    description: str
    assigned_user_id: int | None
    class Config:
        from_attributes = True