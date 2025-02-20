from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.validations import get_current_user
from src.db.database import get_db
from src.db.models import User
from src.services.auth import AuthService
from src.services.user import UserService

bearer_scheme = HTTPBearer()


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)


async def get_current_user_for_access(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    user_service: UserService = Depends(get_user_service),
) -> User:
    return await get_current_user(
        token_type="access", credentials=credentials, user_service=user_service
    )


async def get_current_user_for_refresh(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    user_service: UserService = Depends(get_user_service),
) -> User:
    return await get_current_user(
        token_type="refresh",
        credentials=credentials,
        user_service=user_service,
    )


def admin_required(
    current_user: User = Depends(get_current_user_for_access),
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    return current_user


def superuser_required(
    current_user: User = Depends(get_current_user_for_access),
) -> User:
    if current_user.is_superuser is not True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    return current_user
