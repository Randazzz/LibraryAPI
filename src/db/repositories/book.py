from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.exceptions import BookAlreadyExistsException
from src.db.models.books import Book


class BookRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, book: Book) -> Book:
        try:
            self.db.add(book)
            await self.db.commit()
            return book
        except IntegrityError:
            await self.db.rollback()
            raise BookAlreadyExistsException()

    async def get_all_with_pagination(
        self, limit: int, offset: int
    ) -> Sequence[Book]:
        stmt = (
            select(Book)
            .options(selectinload(Book.authors), selectinload(Book.genres))
            .order_by(Book.id)
            .offset(offset)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id_or_none(self, book_id: int) -> Book | None:
        stmt = (
            select(Book)
            .options(selectinload(Book.authors), selectinload(Book.genres))
            .filter(Book.id == book_id)  # type: ignore
        )
        result = await self.db.execute(stmt)
        book = result.scalars().first()
        return book if book else None

    async def update(self, book: Book) -> None:
        await self.db.commit()
        await self.db.refresh(book)

    async def delete(self, book: Book) -> None:
        await self.db.delete(book)
        await self.db.commit()
