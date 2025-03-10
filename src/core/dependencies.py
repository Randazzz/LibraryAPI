from typing import Callable, Type, TypeVar

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import PermissionDeniedException
from src.core.validations import get_current_user
from src.db.database import get_db
from src.db.models import User
from src.services.auth import AuthService
from src.services.author import AuthorService
from src.services.book import BookService
from src.services.genre import GenreService
from src.services.user import UserService

bearer_scheme = HTTPBearer()


T = TypeVar("T")


def get_service(service_class: Type[T]) -> Callable[[AsyncSession], T]:
    def _get_service(db: AsyncSession = Depends(get_db)) -> T:
        return service_class(db)

    return _get_service


get_user_service = get_service(UserService)
get_auth_service = get_service(AuthService)
get_author_service = get_service(AuthorService)
get_genre_service = get_service(GenreService)
get_book_service = get_service(BookService)


async def get_current_user_for_access(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    user_service: UserService = Depends(get_user_service),
) -> User:
    return await get_current_user(
        expected_token_type="access",
        credentials=credentials,
        user_service=user_service,
    )


async def get_current_user_for_refresh(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    user_service: UserService = Depends(get_user_service),
) -> User:
    return await get_current_user(
        expected_token_type="refresh",
        credentials=credentials,
        user_service=user_service,
    )


def admin_required(
    current_user: User = Depends(get_current_user_for_access),
) -> User:
    if current_user.role != "admin":
        raise PermissionDeniedException()
    return current_user


def superuser_required(
    current_user: User = Depends(get_current_user_for_access),
) -> User:
    if current_user.is_superuser is not True:
        raise PermissionDeniedException()
    return current_user
