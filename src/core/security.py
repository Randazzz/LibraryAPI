from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi.encoders import jsonable_encoder

from src.core.config import settings


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password


def verify_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)


def create_token(data, expires_delta: timedelta, token_type: str) -> str:
    to_encode = jsonable_encoder(data).copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def create_access_token(data) -> str:
    access_token_expires = timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return create_token(data, access_token_expires, "access")


def create_refresh_token(data) -> str:
    refresh_token_expires = timedelta(
        days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
    )
    return create_token(data, refresh_token_expires, "refresh")
