import logging

from fastapi import APIRouter, Depends
from starlette import status

from src.core.dependencies import admin_required, get_genre_service
from src.db.models import User
from src.schemas.genre import GenreCreate, GenreResponse
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
