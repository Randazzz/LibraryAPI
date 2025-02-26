import uuid
from typing import Any, Optional, Sequence

from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy import Row, RowMapping, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import UserNotFoundException
from src.db.models.users import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: User) -> User:
        try:
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except IntegrityError as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists.",
            )

    async def get_by_email(self, email: EmailStr) -> User:
        stmt = select(User).filter(User.email == email)  # type: ignore
        result = await self.db.execute(stmt)
        user = result.scalars().first()
        if not user:
            raise UserNotFoundException()
        return user

    async def get_by_id(self, user_id: uuid.UUID) -> User:
        stmt = select(User).filter(User.id == user_id)  # type: ignore
        result = await self.db.execute(stmt)
        user = result.scalars().first()
        if not user:
            raise UserNotFoundException()
        return user

    async def update_user(self, user: User) -> None:
        await self.db.commit()
        await self.db.refresh(user)

    async def get_users(self, limit: int, offset: int) -> Sequence[User]:
        stmt = select(User).order_by(User.email).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()
