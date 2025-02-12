from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import hash_password
from src.db.models.users import Role, User
from src.db.repositories.user import UserRepository
from src.schemas.users import UserCreate, UserResponse


class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def create_user(
        self, create_user: UserCreate, role: Role = "READER"
    ) -> UserResponse:
        hashed_password = hash_password(create_user.password)
        user = User(
            email=create_user.email,
            first_name=create_user.first_name,
            last_name=create_user.last_name,
            hashed_password=hashed_password,
            role=role,
        )
        created_user = await self.user_repo.create(user)
        return UserResponse(
            id=created_user.id,
            email=created_user.email,
            first_name=created_user.first_name,
            last_name=created_user.last_name,
            role=created_user.role,
        )
