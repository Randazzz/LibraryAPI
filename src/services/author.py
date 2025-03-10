from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import AuthorNotFoundException
from src.db.models.books import Author
from src.db.repositories.author import AuthorRepository
from src.schemas.author import AuthorCreate, AuthorResponse


class AuthorService:
    def __init__(self, db: AsyncSession):
        self.author_repo = AuthorRepository(db)

    async def create_author(self, author_data: AuthorCreate) -> AuthorResponse:
        author = Author(
            name=author_data.name,
            biography=author_data.biography,
            birth_date=author_data.birth_date,
        )
        created_author = await self.author_repo.create(author)
        return AuthorResponse.model_validate(created_author)

    async def get_authors(
        self, limit: int, offset: int
    ) -> list[AuthorResponse]:
        authors = await self.author_repo.get_authors(
            limit=limit, offset=offset
        )
        return [AuthorResponse.model_validate(author) for author in authors]

    async def get_author_by_id(self, user_id: int) -> Author:
        author = await self.author_repo.get_by_id(user_id)
        if author is None:
            raise AuthorNotFoundException()
        return author

    async def update_author_data(self, author_id, new_data) -> AuthorResponse:
        author = await self.get_author_by_id(author_id)
        for key, value in new_data.model_dump(
            exclude_none=True, exclude_unset=True
        ).items():
            setattr(author, key, value)
        await self.author_repo.update_author(author)
        return AuthorResponse.model_validate(author)

    async def delete_author(self, author_id):
        author = await self.get_author_by_id(author_id)
        await self.author_repo.delete_author(author)
        return author

    async def get_by_ids_or_raise(self, author_ids: list[int]) -> list[Author]:
        authors = await self.author_repo.get_by_ids_or_none(author_ids)
        if authors is None:
            raise AuthorNotFoundException()
        return authors
