from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import create_access_token, create_refresh_token
from src.core.exceptions import InvalidCredentialException
from src.core.security import verify_password
from src.db.repositories.user import UserRepository
from src.schemas.auth import AccessToken, TokenPair
from src.schemas.users import UserLogin


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def login(self, user_data: UserLogin) -> TokenPair:
        db_user = await self.user_repo.get_by_email_or_none(user_data.email)
        if not db_user or not verify_password(
            user_data.password, db_user.hashed_password
        ):
            raise InvalidCredentialException()

        access_token = create_access_token(data={"sub": db_user.id})
        refresh_token = create_refresh_token(data={"sub": db_user.id})
        return TokenPair(
            access_token=access_token, refresh_token=refresh_token
        )

    @staticmethod
    async def refresh_jwt(data: dict) -> AccessToken:
        access_token = create_access_token(data=data)
        return AccessToken(access_token=access_token)
