import logging

from fastapi import APIRouter, Depends, Query
from starlette import status

from src.core.dependencies import admin_required, get_genre_service
from src.db.models import User
from src.schemas.common import PaginationParams
from src.schemas.genre import GenreCreate, GenreDeleteResponse, GenreResponse
from src.services.genre import GenreService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/genres", tags=["Genres"])


@router.post(
    "/create",
    response_model=GenreResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new genre",
)
async def create_genre(
    genre_data: GenreCreate,
    current_user: User = Depends(admin_required),
    genre_service: GenreService = Depends(get_genre_service),
) -> GenreResponse:
    genre = await genre_service.create(genre_data)
    logger.info(f"Пользователь {current_user} добавил жанр '{genre}'")
    return genre


@router.get(
    "",
    response_model=list[GenreResponse],
    status_code=status.HTTP_200_OK,
    summary="Genre list",
)
async def get_genres(
    pagination_params: PaginationParams = Query(),
    genre_service: GenreService = Depends(get_genre_service),
) -> list[GenreResponse]:
    return await genre_service.get_all_with_pagination(
        limit=pagination_params.limit, offset=pagination_params.offset
    )


@router.delete(
    "/delete/{genre_id}",
    response_model=GenreDeleteResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete genre by id",
)
async def delete_genre(
    genre_id: int,
    current_user: User = Depends(admin_required),
    genre_service: GenreService = Depends(get_genre_service),
) -> GenreDeleteResponse:
    genre = await genre_service.delete(genre_id)
    logger.info(f"Пользователь {current_user} удалил жанр '{genre}'")
    return GenreDeleteResponse()
