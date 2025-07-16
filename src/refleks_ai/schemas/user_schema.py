
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None


class UserInDB(BaseModel):
    id: int
    email: EmailStr
    username: Optional[str] = None

    class Config:
        from_attributes = True
