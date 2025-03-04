import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import UserNotFoundException
from src.core.security import hash_password
from src.db.models.users import Role, User
from src.db.repositories.user import UserRepository
from src.schemas.users import UserCreate, UserResponse, UserUpdate


class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def create_user(
        self, user_data: UserCreate, role: Role = "READER"
    ) -> UserResponse:
        hashed_password = hash_password(user_data.password)
        user = User(
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            hashed_password=hashed_password,
            role=role,
        )
        created_user = await self.user_repo.create(user)
        return UserResponse.model_validate(created_user)

    async def get_user_by_id(self, user_id: uuid.UUID) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundException()
        return user

    async def change_user_role(
        self, user_id: uuid.UUID, new_role: Role
    ) -> UserResponse:
        user = await self.get_user_by_id(user_id)
        user.role = new_role
        await self.user_repo.update_user(user)
        return UserResponse.model_validate(user)

    async def update_user_data(
        self, user_id: uuid.UUID, new_data: UserUpdate
    ) -> UserResponse:
        user = await self.get_user_by_id(user_id)
        for key, value in new_data.model_dump(
            exclude_none=True, exclude_unset=True
        ).items():
            setattr(user, key, value)
        await self.user_repo.update_user(user)
        return UserResponse.model_validate(user)

    async def get_users(self, limit: int, offset: int) -> list[UserResponse]:
        users = await self.user_repo.get_users(limit=limit, offset=offset)
        return [UserResponse.model_validate(user) for user in users]

    @staticmethod
    async def user_to_user_response(user: User) -> UserResponse:
        return UserResponse.model_validate(user)
