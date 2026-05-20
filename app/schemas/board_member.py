from pydantic import BaseModel
from app.schemas.user import UserSimpleResponse

class BoardMemberResponse(BaseModel):
    role: str
    user: UserSimpleResponse
    class Config:
        from_attributes = True