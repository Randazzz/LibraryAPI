import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.db.models.users import User
else:
    User = "User"

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import (
    Base,
    intpk,
    str_16,
    str_32,
    str_64,
    str_256,
    str_1024,
)
from src.db.models.associations import (
    book_author_association,
    book_genre_association,
)
from src.db.models.utils import (
    default_return_utc_datetime,
    get_current_utc_datetime,
)


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[intpk]
    name: Mapped[str_16] = mapped_column(unique=True, nullable=False)
    books: Mapped[list["Book"]] = relationship(
        secondary=book_genre_association, back_populates="genres"
    )

    def __repr__(self):
        return f"<Genre(id={self.id}, name='{self.name}')>"


class Book(Base):
    __tablename__ = "books"

    id: Mapped[intpk]
    title: Mapped[str_64] = mapped_column(nullable=False, unique=True)
    description: Mapped[Optional[str_256]]
    published_at: Mapped[date] = mapped_column(Date, nullable=False)
    authors: Mapped[list["Author"]] = relationship(
        secondary=book_author_association, back_populates="books"
    )
    genres: Mapped[list[Genre]] = relationship(
        secondary=book_genre_association, back_populates="books"
    )
    book_loans: Mapped[list["BookLoan"]] = relationship(
        "BookLoan", back_populates="book"
    )
    available_copies: Mapped[int] = mapped_column(nullable=False, default=0)

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', available_copies={self.available_copies})>"


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[intpk]
    name: Mapped[str_32] = mapped_column(nullable=False, unique=True)
    biography: Mapped[Optional[str_1024]]
    birth_date: Mapped[date] = mapped_column(nullable=False)
    books: Mapped[list["Book"]] = relationship(
        secondary=book_author_association, back_populates="authors"
    )

    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}', birth_date='{self.birth_date.isoformat()}')>"


class BookLoan(Base):
    __tablename__ = "book_loans"

    id: Mapped[intpk]
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id"), nullable=False
    )
    book: Mapped["Book"] = relationship("Book", back_populates="book_loans")
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="book_loans")
    loan_date: Mapped[datetime] = mapped_column(
        nullable=False, default=get_current_utc_datetime
    )
    return_date: Mapped[datetime] = mapped_column(
        nullable=False, default=default_return_utc_datetime
    )
    returned: Mapped[bool] = mapped_column(nullable=False, default=False)

    def __repr__(self):
        return f"<Loan(id={self.id}, book_id={self.book_id}, user_id={self.user_id}, returned={self.returned})>"
