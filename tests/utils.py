from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import create_access_token, create_refresh_token
from src.core.security import hash_password
from src.db.models import User
from src.db.models.users import Role
from src.schemas.users import UserCreateResponseTest


async def create_user(
    session: AsyncSession,
    email: EmailStr,
    password: str,
    role: Role = None,
    is_superuser: bool = False,
) -> UserCreateResponseTest:
    hashed_password = hash_password(password)
    user = User(
        email=email,
        first_name="some",
        last_name="user",
        hashed_password=hashed_password,
        role=role,
        is_superuser=is_superuser,
    )
    session.add(user)
    await session.commit()
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    return UserCreateResponseTest(
        id=user.id,
        email=email,
        password=password,
        access_token=access_token,
        refresh_token=refresh_token,
    )
