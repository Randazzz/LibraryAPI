import logging

from fastapi import APIRouter, Depends, Query, status

from src.core.dependencies import admin_required, get_book_service
from src.db.models import User
from src.schemas.book import (
    BookCreate,
    BookDeleteResponse,
    BookResponse,
    BookUpdate,
    BookLoanCreate, BookLoanResponse,
)
from src.services.book import BookService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/books", tags=["Books"])


@router.post(
    "/create",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new book",
)
async def create_book(
    book_data: BookCreate,
    current_user: User = Depends(admin_required),
    book_service: BookService = Depends(get_book_service),
) -> BookResponse:
    book = await book_service.create(book_data)
    logger.info(f"Пользователь {current_user} добавил книгу '{book}'")
    return book


@router.get(
    "",
    response_model=list[BookResponse],
    status_code=status.HTTP_200_OK,
    summary="Book list",
)
async def get_books(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    book_service: BookService = Depends(get_book_service),
) -> list[BookResponse]:
    return await book_service.get_all_with_pagination(
        limit=limit, offset=offset
    )


@router.patch(
    "/update/{book_id}",
    response_model=BookResponse,
    status_code=status.HTTP_200_OK,
    summary="Update book by id",
)
async def update_book(
    book_id: int,
    new_data: BookUpdate,
    current_user: User = Depends(admin_required),
    book_service: BookService = Depends(get_book_service),
) -> BookResponse:
    book = await book_service.update(book_id, new_data)
    logger.info(f"Пользователь {current_user} изменил книгу '{book}'")
    return book


@router.delete(
    "/delete/{book_id}",
    response_model=BookDeleteResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete book by id",
)
async def delete_book(
    book_id: int,
    current_user: User = Depends(admin_required),
    book_service: BookService = Depends(get_book_service),
) -> BookDeleteResponse:
    book = await book_service.delete(book_id)
    logger.info(f"Пользователь {current_user} удалил книгу '{book}'")
    return BookDeleteResponse()


@router.post(
    "/lend",
    response_model=BookLoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Lend a book to a reader",
)
async def lend_book(
    book_loan: BookLoanCreate,
    current_user: User = Depends(admin_required),
    book_service: BookService = Depends(get_book_service),
) -> BookLoanResponse:
    book_loan = await book_service.lend(book_loan)
    logger.info(
        f"Пользователь {current_user} выдал книгу с id '{book_loan.book_id}' читателю c id '{book_loan.user_id}'"
    )
    return book_loan
