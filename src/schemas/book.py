import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.schemas.author import AuthorResponse
from src.schemas.common import PaginationParams
from src.schemas.genre import GenreResponse


class BookBase(BaseModel):
    title: str = Field(..., max_length=64)
    description: Optional[str] = Field(default=None, max_length=256)
    published_at: date
    available_copies: Optional[int] = Field(default=0)


class BookCreate(BookBase):
    author_ids: list[int]
    genre_ids: list[int]

    @field_validator("author_ids", "genre_ids", mode="before")
    def convert_to_list(cls, value):
        if isinstance(value, int):
            return [value]
        return value


class BookResponse(BookBase):
    id: int
    authors: list[AuthorResponse]
    genres: list[GenreResponse]

    model_config = ConfigDict(from_attributes=True)


class BookResponseWithStats(BookResponse):
    loan_count: int

    model_config = ConfigDict(from_attributes=True)


class BookUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=64)
    description: Optional[str] = Field(default=None, max_length=256)
    published_at: Optional[date] = Field(default=None)
    available_copies: Optional[int] = Field(default=None)
    author_ids: Optional[list[int]] = Field(default=None)
    genre_ids: Optional[list[int]] = Field(default=None)


class BookFilterParams(BaseModel):
    title: Optional[str] = Field(default=None)
    author_ids: Optional[list[int]] = Field(default=None)
    genre_ids: Optional[list[int]] = Field(default=None)


class BookQueryParams(BookFilterParams, PaginationParams):
    pass


class BookDeleteResponse(BaseModel):
    message: Optional[str] = Field(default="Book deleted successfully")


class BookLoanCreate(BaseModel):
    book_id: int
    user_id: uuid.UUID


class BookLoanResponse(BookLoanCreate):
    id: int
    loan_date: datetime
    return_date: datetime
    returned: bool

    model_config = ConfigDict(from_attributes=True)


class BookLoanUpdate(BaseModel):
    return_date: datetime
    returned: bool


class BookLoanReturnResponse(BaseModel):
    message: Optional[str] = Field(default="Book returned successfully")
