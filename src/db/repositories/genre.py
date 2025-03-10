from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

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
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Genre with this name already exists.",
            )

    async def get_by_ids_or_none(self, genre_ids) -> list[Genre] | None:
        stmt = select(Genre).filter(Genre.id.in_(genre_ids))
        result = await self.db.execute(stmt)
        genres = result.scalars().all()
        return genres if genres else None
