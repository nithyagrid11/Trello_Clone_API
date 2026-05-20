from pydantic import BaseModel
from app.schemas.board_member import BoardMemberResponse
from app.schemas.section import SectionDetailResponse

class Board(BaseModel):
    name: str
    description: str

class BoardCreate(Board):
    name: str
    description: str

class BoardResponse(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int

    class Config:
        from_attributes = True

class BoardDetailResponse(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int
    invitation_token: str | None = None
    sections: list[SectionDetailResponse]
    members: list[BoardMemberResponse]
    class Config:
        from_attributes = True