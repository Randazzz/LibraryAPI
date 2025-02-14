from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from src.db.repositories.user import UserRepository
from src.schemas.auth import TokenResponse
from src.schemas.users import UserLogin


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def login(self, user_data: UserLogin) -> TokenResponse:
        db_user = await self.user_repo.get_by_email(user_data.email)
        if not db_user or not verify_password(
            user_data.password, db_user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        access_token = create_access_token(
            data={
                "sub": db_user.email,
                "role": db_user.role,
                "is_superuser": db_user.is_superuser,
            },
        )
        refresh_token = create_refresh_token(data={"sub": db_user.email})
        return TokenResponse(
            access_token=access_token, refresh_token=refresh_token
        )
