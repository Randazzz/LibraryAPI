from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db.database import get_db
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
    user_create: UserCreate, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    user_service = UserService(db)
    return await user_service.create_user(user_create)
