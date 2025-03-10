import re
import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from src.db.models.users import Role


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str

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


class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    first_name: str
    last_name: str
    role: Role
    is_superuser: bool

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreateResponseTest(BaseModel):
    id: uuid.UUID
    email: EmailStr
    password: str
    access_token: str
    refresh_token: str
