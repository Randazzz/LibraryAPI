import uuid
from typing import Sequence

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import UserAlreadyExistsException
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
            raise UserAlreadyExistsException()

    async def get_by_email(self, email: EmailStr) -> User | None:
        stmt = select(User).filter(User.email == email)  # type: ignore
        result = await self.db.execute(stmt)
        user = result.scalars().first()
        if not user:
            return None
        return user

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        stmt = select(User).filter(User.id == user_id)  # type: ignore
        result = await self.db.execute(stmt)
        user = result.scalars().first()
        if not user:
            return None
        return user

    async def update_user(self, user: User) -> None:
        await self.db.commit()
        await self.db.refresh(user)

    async def get_users(self, limit: int, offset: int) -> Sequence[User]:
        stmt = select(User).order_by(User.email).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()
