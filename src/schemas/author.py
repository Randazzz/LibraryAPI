from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.schemas.book import Book


class AuthorResponse(BaseModel):
    id: int
    name: str
    biography: Optional[str] = None
    birth_date: date
    books: Optional[list[Book]] = None

    model_config = ConfigDict(from_attributes=True)


class AuthorCreate(BaseModel):
    name: str
    biography: Optional[str] = None
    birth_date: date
    books: Optional[list[Book]] = None
