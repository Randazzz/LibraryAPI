from sqlalchemy import Column, ForeignKey, Integer, Table

from src.db.models.base import Base

book_genre_association = Table(
    "book_genre_association",
    Base.metadata,
    Column(
        "book_id",
        Integer,
        ForeignKey("books.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "genre_id",
        Integer,
        ForeignKey("genres.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

book_author_association = Table(
    "book_author_association",
    Base.metadata,
    Column(
        "book_id",
        Integer,
        ForeignKey("books.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "author_id",
        Integer,
        ForeignKey("authors.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
