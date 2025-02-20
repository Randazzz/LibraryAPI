import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.db.database import get_db
from src.db.models import User
from src.services.auth import AuthService
from src.services.user import UserService

bearer_scheme = HTTPBearer()


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)


async def validate_token(
    token_type: str,
    payload: dict,
) -> None:
    current_token_type = payload.get("type")
    if current_token_type != token_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token type '{current_token_type}' expected '{token_type}'",
        )
    if "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token",
        )


async def get_payload(
    credentials: HTTPAuthorizationCredentials,
    token_type: str,
) -> dict:
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        await validate_token(token_type, payload)
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


async def get_current_user(
    token_type: str,
    credentials: HTTPAuthorizationCredentials,
    user_service: UserService,
) -> User:
    payload = await get_payload(credentials, token_type)
    user = await user_service.get_user_by_id(payload["sub"])
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return user


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
