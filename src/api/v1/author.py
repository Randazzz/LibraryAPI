import logging

from fastapi import APIRouter, Depends, Query, status

from src.core.dependencies import admin_required, get_author_service
from src.db.models import User
from src.schemas.author import (
    AuthorCreate,
    AuthorDeleteResponse,
    AuthorResponse,
    AuthorUpdate,
)
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
    current_user: User = Depends(admin_required),
    author_service: AuthorService = Depends(get_author_service),
) -> AuthorResponse:
    author = await author_service.create_author(author_data)
    logger.info(f"Пользователь {current_user} добавил автора '{author}'")
    return author


@router.get(
    "",
    response_model=list[AuthorResponse],
    status_code=status.HTTP_200_OK,
    summary="Author list",
)
async def get_authors(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    author_service: AuthorService = Depends(get_author_service),
) -> list[AuthorResponse]:
    return await author_service.get_authors(limit=limit, offset=offset)


@router.patch(
    "/update/{author_id}",
    response_model=AuthorResponse,
    status_code=status.HTTP_200_OK,
    summary="Update author for id",
)
async def update_author(
    author_id: int,
    new_data: AuthorUpdate,
    current_user: User = Depends(admin_required),
    author_service: AuthorService = Depends(get_author_service),
) -> AuthorResponse:
    author = await author_service.update_author_data(author_id, new_data)
    logger.info(f"Пользователь {current_user} изменил автора '{author}'")
    return author


@router.delete(
    "/delete/{author_id}",
    response_model=AuthorDeleteResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete author for id",
)
async def delete_author(
    author_id: int,
    current_user: User = Depends(admin_required),
    author_service: AuthorService = Depends(get_author_service),
) -> AuthorDeleteResponse:
    author = await author_service.delete_author(author_id)
    logger.info(f"Пользователь {current_user} удалил автора '{author}'")
    return AuthorDeleteResponse()
