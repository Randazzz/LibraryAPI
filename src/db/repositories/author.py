from fastapi import HTTPException, status
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
