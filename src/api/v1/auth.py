from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core.dependencies import admin_required, get_current_user
from src.db.database import get_db
from src.schemas.auth import TokenResponse
from src.schemas.users import UserLogin
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate user",
)
async def login(
    user_data: UserLogin, db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    auth_service = AuthService(db)
    return await auth_service.login(user_data)


@router.get("/reader")
async def test_jwt(current_user: str = Depends(get_current_user)):
    return {"current_user": current_user}


@router.get("/admin")
async def test_jwt(current_user: str = Depends(admin_required)):
    return {"current_user": current_user}
