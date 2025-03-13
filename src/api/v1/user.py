import logging
import uuid

from fastapi import APIRouter, Depends, Query, status

from src.core.dependencies import (
    admin_required,
    get_current_user_for_access,
    get_user_service,
    superuser_required,
)
from src.db.models.users import Role, User
from src.schemas.common import PaginationParams
from src.schemas.users import UserCreate, UserResponse, UserUpdate, UserResponseWithStats
from src.services.user import UserService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    return await user_service.create(user_data)


@router.patch(
    "/{user_id}/change-role",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Change role on a user",
)
async def change_user_role(
    user_id: uuid.UUID,
    new_role: Role,
    current_user: str = Depends(superuser_required),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    user = await user_service.change_role(user_id, new_role)
    logger.info(
        f"Пользователь {current_user} изменил роль пользователя с id '{user_id}' на {new_role}"
    )
    return user


@router.get(
    "",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="User list",
)
async def get_users(
    pagination_params: PaginationParams = Query(),
    current_user: str = Depends(admin_required),
    user_service: UserService = Depends(get_user_service),
) -> list[UserResponse]:
    return await user_service.get_all_with_pagination(
        limit=pagination_params.limit, offset=pagination_params.offset
    )


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user",
)
async def get_current_user(
    current_user: User = Depends(get_current_user_for_access),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    return await user_service.user_to_user_response(current_user)


@router.patch(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Update current user",
)
async def update_current_user(
    new_data: UserUpdate,
    current_user: User = Depends(get_current_user_for_access),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    return await user_service.update_data(current_user.id, new_data)


@router.get(
    "/statistics/active-users",
    response_model=list[UserResponseWithStats],
    status_code=status.HTTP_200_OK,
    summary="List of users sorted by activity",
)
async def get_active_users(
    params: PaginationParams = Query(),
    current_user: str = Depends(admin_required),
    user_service: UserService = Depends(get_user_service),
) -> list[UserResponseWithStats]:
    return await user_service.get_most_active_users(
        limit=params.limit, offset=params.offset
    )
