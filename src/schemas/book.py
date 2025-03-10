from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from src.schemas.author import AuthorResponse
from src.schemas.genre import GenreResponse


class BookCreate(BaseModel):
    title: str
    description: Optional[str]
    published_at: date
    author_ids: list[int]
    genre_ids: list[int]
    available_copies: int

    @field_validator("author_ids", "genre_ids", mode="before")
    def convert_to_list(cls, value):
        if isinstance(value, int):
            return [value]
        return value


class BookResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    published_at: date
    authors: list[AuthorResponse]
    genres: list[GenreResponse]
    available_copies: int

    model_config = ConfigDict(from_attributes=True)
