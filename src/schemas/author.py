from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AuthorResponse(BaseModel):
    id: int
    name: str
    biography: Optional[str] = None
    birth_date: date

    model_config = ConfigDict(from_attributes=True)


class AuthorCreate(BaseModel):
    name: str
    biography: Optional[str] = None
    birth_date: date


class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    biography: Optional[str] = None
    birth_date: Optional[date] = None


class AuthorDeleteResponse(BaseModel):
    message: Optional[str] = "Author deleted successfully"


class AuthorCreateResponseTest(BaseModel):
    id: int
    name: str
    biography: Optional[str] = None
    birth_date: date
