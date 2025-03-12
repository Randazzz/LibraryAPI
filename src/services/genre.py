from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import GenreNotFoundException
from src.db.models.books import Genre
from src.db.repositories.genre import GenreRepository
from src.schemas.genre import GenreCreate, GenreResponse


class GenreService:
    def __init__(self, db: AsyncSession):
        self.genre_repo = GenreRepository(db)

    async def create(self, genre_data: GenreCreate) -> GenreResponse:
        genre = Genre(
            name=genre_data.name,
        )
        created_genre = await self.genre_repo.create(genre)
        return GenreResponse.model_validate(created_genre)

    async def get_by_ids_or_raise(self, genre_ids: list[int]) -> list[Genre]:
        genres = await self.genre_repo.get_by_ids_or_none(genre_ids)
        if genres is None:
            raise GenreNotFoundException()
        return genres

    async def get_by_id_or_raise(self, genre_id: int) -> Genre:
        genre = await self.genre_repo.get_by_id_or_none(genre_id)
        if genre is None:
            raise GenreNotFoundException()
        return genre

    async def get_all_with_pagination(
        self, limit: int, offset: int
    ) -> list[GenreResponse]:
        genres = await self.genre_repo.get_all_with_pagination(
            limit=limit, offset=offset
        )
        return [GenreResponse.model_validate(genre) for genre in genres]

    async def delete(self, genre_id: int) -> None:
        genre = await self.get_by_id_or_raise(genre_id)
        await self.genre_repo.delete(genre)
