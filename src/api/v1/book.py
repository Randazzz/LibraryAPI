import logging

from fastapi import APIRouter, Depends, status

from src.core.dependencies import admin_required, get_book_service
from src.db.models import User
from src.schemas.book import BookCreate, BookResponse
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
    book = await book_service.create_book(book_data)
    logger.info(f"Пользователь {current_user} добавил книгу '{book}'")
    return book
