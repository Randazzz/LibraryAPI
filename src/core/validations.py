import jwt
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from starlette import status

from src.core.config import settings
from src.core.exceptions import InvalidTokenException
from src.db.models import User
from src.services.user import UserService


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
        raise InvalidTokenException()


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
        raise InvalidTokenException()


async def get_current_user(
    token_type: str,
    credentials: HTTPAuthorizationCredentials,
    user_service: UserService,
) -> User:
    payload = await get_payload(credentials, token_type)
    user = await user_service.get_user_by_id(payload["sub"])
    return user
