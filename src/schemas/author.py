from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AuthorCreate(BaseModel):
    name: str = Field(..., max_length=32)
    biography: Optional[str] = Field(default=None, max_length=1024)
    birth_date: date


class AuthorResponse(AuthorCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=32)
    biography: Optional[str] = Field(default=None, max_length=1024)
    birth_date: Optional[date] = Field(default=None)


class AuthorDeleteResponse(BaseModel):
    message: Optional[str] = Field(default="Author deleted successfully")
