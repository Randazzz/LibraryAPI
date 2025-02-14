import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core.security import superuser_required
from src.db.database import get_db
from src.db.models.users import Role
from src.schemas.users import UserCreate, UserResponse
from src.services.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register(
    user_data: UserCreate, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    user_service = UserService(db)
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
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    user_service = UserService(db)
    return await user_service.change_user_role(user_id, new_role)
