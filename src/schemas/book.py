import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.schemas.author import AuthorResponse
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


class BookUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=64)
    description: Optional[str] = Field(default=None, max_length=256)
    published_at: Optional[date] = Field(default=None)
    available_copies: Optional[int] = Field(default=None)
    author_ids: Optional[list[int]] = Field(default=None)
    genre_ids: Optional[list[int]] = Field(default=None)


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

    # id: Mapped[intpk]
    # book_id: Mapped[int] = mapped_column(
    #     ForeignKey("books.id"), nullable=False
    # )
    # book: Mapped["Book"] = relationship("Book", back_populates="book_loans")
    # user_id: Mapped[uuid.UUID] = mapped_column(
    #     ForeignKey("users.id"), nullable=False
    # )
    # user: Mapped["User"] = relationship("User", back_populates="book_loans")
    # loan_date: Mapped[datetime] = mapped_column(
    #     nullable=False, default=get_current_utc_datetime
    # )
    # return_date: Mapped[datetime] = mapped_column(
    #     nullable=False, default=default_return_utc_datetime
    # )
    # returned: Mapped[bool] = mapped_column(nullable=False, default=False)
