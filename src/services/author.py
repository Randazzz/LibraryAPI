from sqlalchemy.ext.asyncio import AsyncSession

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
            books=author_data.books,
        )
        created_author = await self.author_repo.create(author)
        return AuthorResponse.model_validate(created_author)
