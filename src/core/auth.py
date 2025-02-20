from datetime import datetime, timedelta, timezone

import jwt
from fastapi.encoders import jsonable_encoder

from src.core.config import settings


def create_token(data: dict, expires_delta: timedelta, token_type: str) -> str:
    to_encode = jsonable_encoder(data).copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def create_access_token(data: dict) -> str:
    access_token_expires = timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return create_token(data, access_token_expires, "access")


def create_refresh_token(data: dict) -> str:
    refresh_token_expires = timedelta(
        days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
    )
    return create_token(data, refresh_token_expires, "refresh")
