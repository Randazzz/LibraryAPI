from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.books import Author


class AuthorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, author: Author) -> Author:
        try:
            self.db.add(author)
            await self.db.commit()
            await self.db.refresh(author)
            return author
        except IntegrityError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Author with this name already exists.",
            )

    async def get_authors(self, limit: int, offset: int) -> Sequence[Author]:
        stmt = select(Author).order_by(Author.id).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, author_id: int) -> Author | None:
        stmt = select(Author).filter(Author.id == author_id)  # type: ignore
        result = await self.db.execute(stmt)
        author = result.scalars().first()
        if not author:
            return None
        return author

    async def update_author(self, author: Author) -> None:
        await self.db.commit()
        await self.db.refresh(author)

    async def delete_author(self, author: Author) -> None:
        await self.db.delete(author)
        await self.db.commit()
