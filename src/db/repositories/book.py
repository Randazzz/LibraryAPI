from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

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
