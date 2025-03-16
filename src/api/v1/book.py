import logging

from fastapi import APIRouter, Depends, Query, status
from fastapi_cache.decorator import cache

from src.core.dependencies import (
    admin_required,
    get_book_service,
    get_current_user_for_access,
)
from src.db.models import User
from src.schemas.book import (
    BookCreate,
    BookDeleteResponse,
    BookLoanCreate,
    BookLoanResponse,
    BookLoanReturnResponse,
    BookQueryParams,
    BookResponse,
    BookResponseWithStats,
    BookUpdate,
)
from src.schemas.common import PaginationParams
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
    summary="Book list with filtering and pagination",
)
@cache(expire=60)
async def get_books(
    params: BookQueryParams = Query(),
    book_service: BookService = Depends(get_book_service),
) -> list[BookResponse]:
    return await book_service.get_all_with_pagination_and_filtration(params)


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


@router.post(
    "/return-book/{loan_id}",
    response_model=BookLoanReturnResponse,
    status_code=status.HTTP_200_OK,
    summary="Return the book",
)
async def return_book(
    loan_id: int,
    current_user: User = Depends(get_current_user_for_access),
    book_service: BookService = Depends(get_book_service),
) -> BookLoanReturnResponse:
    book_loan = await book_service.return_book(loan_id, current_user.id)
    logger.info(
        f"Пользователь {current_user} вернул книгу с id '{book_loan.book_id}'"
    )
    return BookLoanReturnResponse()


@router.get(
    "/statistics/popular-books",
    response_model=list[BookResponseWithStats],
    status_code=status.HTTP_200_OK,
    summary="List of books sorted by popularity",
)
@cache(expire=60)
async def get_popular_books(
    params: PaginationParams = Query(),
    book_service: BookService = Depends(get_book_service),
) -> list[BookResponseWithStats]:
    return await book_service.get_most_popular_books(
        limit=params.limit, offset=params.offset
    )
