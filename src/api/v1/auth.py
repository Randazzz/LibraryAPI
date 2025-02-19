from fastapi import APIRouter, Depends
from starlette import status

from src.core.dependencies import (
    get_auth_service,
    get_current_user_for_refresh,
)
from src.core.security import create_access_token
from src.db.models import User
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
    user_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    return await auth_service.login(user_data)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
)
async def refresh_jwt(
    current_user: User = Depends(get_current_user_for_refresh),
) -> TokenResponse:
    access_token = create_access_token(data={"sub": current_user.id})
    return TokenResponse(access_token=access_token)
