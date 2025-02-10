import uuid

from pydantic import BaseModel, EmailStr

from src.db.models.users import Role


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str


class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    first_name: str
    last_name: str
    role: Role


class UserLogin(BaseModel):
    email: EmailStr
    password: str
