from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.users import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_email(self, email: EmailStr) -> User | None:
        stmt = select(User).filter(User.email == email)  # type: ignore
        result = await self.db.execute(stmt)
        return result.scalars().first()
