import re
import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from src.db.models.users import Role


class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., max_length=16)
    last_name: str = Field(..., max_length=16)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=16)

    # fmt: off
    @field_validator("password")
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", password):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[\W_]", password):
            raise ValueError("Password must contain at least one special character")
        return password
    # fmt: on


class UserResponse(UserBase):
    id: uuid.UUID
    role: Role
    is_superuser: bool

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(default=None, max_length=16)
    last_name: Optional[str] = Field(default=None, max_length=16)


class UserCreateResponseTest(BaseModel):
    id: uuid.UUID
    email: EmailStr
    password: str
    access_token: str
    refresh_token: str
