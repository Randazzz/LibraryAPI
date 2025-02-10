from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core.security import get_current_user
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
    user: UserLogin, db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    auth_service = AuthService(db)
    return await auth_service.login(user)


# @router.get("/reader")
# async def test_jwt(current_user: str = Depends(get_current_user)):
#
#     return {"email": current_user, "private_info": "you reader 52"}
#
#
# @router.get("/admin")
# async def test_jwt():
#     return {"private_info": "you admin 52"}
