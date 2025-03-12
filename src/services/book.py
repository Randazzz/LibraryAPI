from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.not_found import BookNotFoundException
from src.db.models.books import Author, Book, Genre
from src.db.repositories.book import BookRepository
from src.schemas.book import BookCreate, BookResponse, BookUpdate
from src.services.author import AuthorService
from src.services.genre import GenreService


class BookService:
    def __init__(self, db: AsyncSession):
        self.book_repo = BookRepository(db)
        self.author_service = AuthorService(db)
        self.genre_service = GenreService(db)

    async def create(self, book_data: BookCreate) -> BookResponse:
        authors: list[Author] = await self.author_service.get_by_ids_or_raise(
            book_data.author_ids
        )
        genres: list[Genre] = await self.genre_service.get_by_ids_or_raise(
            book_data.genre_ids
        )
        book = Book(
            title=book_data.title,
            description=book_data.description,
            published_at=book_data.published_at,
            authors=authors,
            genres=genres,
            available_copies=book_data.available_copies,
        )
        created_book = await self.book_repo.create(book)
        return BookResponse.model_validate(created_book)

    async def get_all_with_pagination(
        self, limit: int, offset: int
    ) -> list[BookResponse]:
        books = await self.book_repo.get_all_with_pagination(
            limit=limit, offset=offset
        )
        return [BookResponse.model_validate(book) for book in books]

    async def get_by_id_or_raise(self, book_id: int) -> Book:
        book = await self.book_repo.get_by_id_or_none(book_id)
        if book is None:
            raise BookNotFoundException()
        return book

    async def update(self, book_id: int, new_data: BookUpdate) -> BookResponse:
        book = await self.get_by_id_or_raise(book_id)
        if new_data.author_ids:
            book.authors = await self.author_service.get_by_ids_or_raise(
                new_data.author_ids
            )
        if new_data.genre_ids:
            book.genres = await self.genre_service.get_by_ids_or_raise(
                new_data.genre_ids
            )
        for key, value in new_data.model_dump(
            exclude_none=True, exclude_unset=True
        ).items():
            setattr(book, key, value)
        await self.book_repo.update(book)
        return BookResponse.model_validate(book)

    async def delete(self, book_id) -> None:
        book = await self.get_by_id_or_raise(book_id)
        await self.book_repo.delete(book)
