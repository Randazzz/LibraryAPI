import uuid
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.exceptions.limit_exceeded import BookLimitExceededException
from src.core.exceptions.not_found import (
    BookCopyNotFoundException,
    BookLoanNotFoundException,
    BookNotFoundException,
)
from src.db.models.books import Author, Book, BookLoan, Genre
from src.db.repositories.book import BookRepository
from src.schemas.book import (
    BookCreate,
    BookFilterParams,
    BookLoanCreate,
    BookLoanResponse,
    BookLoanUpdate,
    BookQueryParams,
    BookResponse,
    BookUpdate,
)
from src.services.author import AuthorService
from src.services.genre import GenreService
from src.services.user import UserService


class BookService:
    def __init__(self, db: AsyncSession):
        self.book_repo = BookRepository(db)
        self.author_service = AuthorService(db)
        self.genre_service = GenreService(db)
        self.user_service = UserService(db)

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

    async def get_all_with_pagination_and_filtration(
        self, params: BookQueryParams
    ) -> list[BookResponse]:
        filters = BookFilterParams.model_validate(params).model_dump(
            exclude_none=True, exclude_unset=True
        )
        books = await self.book_repo.get_all_with_pagination_and_filtration(
            limit=params.limit, offset=params.offset, filters=filters
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
        updated_book = await self.get_by_id_or_raise(book.id)
        return BookResponse.model_validate(updated_book)

    async def delete(self, book_id) -> None:
        book = await self.get_by_id_or_raise(book_id)
        await self.book_repo.delete(book)

    async def get_book_loan_by_id_or_raise(
        self, book_loan_id: int
    ) -> BookLoan:
        book_loan = await self.book_repo.get_book_loan_by_id_or_none(
            book_loan_id
        )
        if book_loan is None:
            raise BookLoanNotFoundException()
        return book_loan

    async def get_book_loans_by_user_id(
        self, user_id: uuid.UUID
    ) -> list[BookLoan]:
        return await self.book_repo.get_book_loans_by_user_id(user_id)

    async def update_book_loan(
        self, book_loan_id: int, new_data: BookLoanUpdate
    ) -> BookLoanResponse:
        book_loan = await self.get_book_loan_by_id_or_raise(book_loan_id)
        for key, value in new_data.model_dump(
            exclude_none=True, exclude_unset=True
        ).items():
            setattr(book_loan, key, value)
        await self.book_repo.update_book_loan(book_loan)
        return BookLoanResponse.model_validate(book_loan)

    async def lend(self, book_loan: BookLoanCreate) -> BookLoanResponse:
        book = await self.get_by_id_or_raise(book_loan.book_id)
        if book.available_copies <= 0:
            raise BookCopyNotFoundException()
        user = await self.user_service.get_by_id_or_raise(book_loan.user_id)
        users_book_loans = await self.get_book_loans_by_user_id(user.id)
        if len(users_book_loans) >= settings.BOOK_LIMIT_FOR_USER:
            raise BookLimitExceededException()
        book_loan = BookLoan(book_id=book.id, user_id=user.id)
        created_book_loan = await self.book_repo.create_book_loan(book_loan)
        book.available_copies -= 1
        await self.book_repo.update(book)
        return BookLoanResponse.model_validate(created_book_loan)

    async def return_book(
        self, loan_id: int, user_id: uuid.UUID
    ) -> BookLoanResponse:
        book_loan = await self.get_book_loan_by_id_or_raise(loan_id)
        if user_id != book_loan.user_id or book_loan.returned:
            raise BookLoanNotFoundException()
        book_loan_new_data = BookLoanUpdate(
            returned=True,
            return_date=datetime.now(UTC).replace(tzinfo=None),
        )
        updated_book_loan = await self.update_book_loan(
            loan_id, book_loan_new_data
        )
        book = book_loan.book
        book_new_data = BookUpdate(available_copies=book.available_copies + 1)
        await self.update(book.id, book_new_data)
        return BookLoanResponse.model_validate(updated_book_loan)
