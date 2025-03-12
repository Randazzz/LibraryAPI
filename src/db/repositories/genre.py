from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import GenreAlreadyExistsException
from src.db.models.books import Genre


class GenreRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, genre: Genre) -> Genre:
        try:
            self.db.add(genre)
            await self.db.commit()
            await self.db.refresh(genre)
            return genre
        except IntegrityError:
            await self.db.rollback()
            raise GenreAlreadyExistsException()

    async def get_by_ids_or_none(
        self, genre_ids: list[int]
    ) -> list[Genre] | None:
        stmt = select(Genre).filter(Genre.id.in_(genre_ids))
        result = await self.db.execute(stmt)
        genres = result.scalars().all()
        return genres if genres else None

    async def get_by_id_or_none(self, genre_id: int) -> Genre | None:
        stmt = select(Genre).filter(Genre.id == genre_id)  # type: ignore
        result = await self.db.execute(stmt)
        genre = result.scalars().first()
        return genre if genre else None

    async def get_all_with_pagination(
        self, limit: int, offset: int
    ) -> Sequence[Genre]:
        stmt = select(Genre).order_by(Genre.id).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def delete(self, genre: Genre) -> None:
        await self.db.delete(genre)
        await self.db.commit()
