import uuid
from typing import List

from fastapi import APIRouter, Depends, Query
from starlette import status

from src.core.dependencies import (
    admin_required,
    get_current_user,
    get_user_service,
    superuser_required,
)
from src.db.models.users import Role, User
from src.schemas.users import UserCreate, UserResponse, UserUpdate
from src.services.user import UserService

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
    return await user_service.create_user(user_data)


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
    return await user_service.change_user_role(user_id, new_role)


@router.get(
    "/",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="User list",
)
async def get_users(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: str = Depends(admin_required),
    user_service: UserService = Depends(get_user_service),
) -> List[UserResponse]:
    return await user_service.get_users(limit=limit, offset=offset)


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user",
)
async def get_current_user(
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    return user_service.user_to_user_response(current_user)


@router.patch(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Update current user",
)
async def update_current_user(
    new_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    return await user_service.update_user_data(current_user.id, new_data)
