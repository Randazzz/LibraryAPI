from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.books import Author, Book, Genre
from src.db.repositories.book import BookRepository
from src.schemas.book import BookCreate, BookResponse
from src.services.author import AuthorService
from src.services.genre import GenreService


class BookService:
    def __init__(self, db: AsyncSession):
        self.book_repo = BookRepository(db)
        self.author_service = AuthorService(db)
        self.genre_service = GenreService(db)

    async def create_book(self, book_data: BookCreate) -> BookResponse:
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
