import logging

from fastapi import APIRouter, Depends, Query, status

from src.core.dependencies import admin_required, get_author_service
from src.schemas.author import AuthorCreate, AuthorResponse
from src.services.author import AuthorService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post(
    "/create",
    response_model=AuthorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new author",
)
async def create(
    author_data: AuthorCreate,
    current_user: str = Depends(admin_required),
    author_service: AuthorService = Depends(get_author_service),
) -> AuthorResponse:
    author = await author_service.create_author(author_data)
    logger.info(f"Пользователь {current_user} добавил автора '{author}'")
    return author


# @router.get(
#     "",
#     response_model=list[AuthorResponse],
#     status_code=status.HTTP_200_OK,
#     summary="Author list",
# )
# async def get_authors(
#     limit: int = Query(10, ge=1, le=100),
#     offset: int = Query(0, ge=0),
#     author_service: AuthorService = Depends(get_author_service),
# ) -> list[AuthorResponse]:
#     return await author_service.get_authors(limit=limit, offset=offset)
