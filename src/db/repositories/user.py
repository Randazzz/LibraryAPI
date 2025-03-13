import uuid
from typing import Sequence

from pydantic import EmailStr
from sqlalchemy import select, Row, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import UserAlreadyExistsException
from src.db.models import BookLoan
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

    async def get_by_email_or_none(self, email: EmailStr) -> User | None:
        stmt = select(User).filter(User.email == email)  # type: ignore
        result = await self.db.execute(stmt)
        user = result.scalars().first()
        if not user:
            return None
        return user

    async def get_by_id_or_none(self, user_id: uuid.UUID) -> User | None:
        stmt = select(User).filter(User.id == user_id)  # type: ignore
        result = await self.db.execute(stmt)
        user = result.scalars().first()
        if not user:
            return None
        return user

    async def get_all_with_pagination(
        self, limit: int, offset: int
    ) -> Sequence[User]:
        stmt = select(User).order_by(User.email).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_most_active_users(
        self, limit: int, offset: int
    ) -> Sequence[Row[tuple[User, int]]]:
        subquery = (
            select(
                BookLoan.user_id, func.count(BookLoan.id).label("loan_count")
            )
            .group_by(BookLoan.user_id)
            .subquery()
        )

        stmt = (
            select(User, func.coalesce(subquery.c.loan_count, 0))
            .outerjoin(subquery, User.id == subquery.c.user_id)
            .order_by(subquery.c.loan_count.desc().nullslast(), User.id)
            .offset(offset)
            .limit(limit)
        )

        result = await self.db.execute(stmt)
        return result.all()

    async def update(self, user: User) -> None:
        await self.db.commit()
        await self.db.refresh(user)
