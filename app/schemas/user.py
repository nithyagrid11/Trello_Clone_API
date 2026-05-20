from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserSimpleResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    class Config:
        from_attributes = True