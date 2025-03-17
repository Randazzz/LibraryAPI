from datetime import datetime
from typing import AsyncGenerator

import pytest
from faker import Faker
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from httpx import ASGITransport, AsyncClient
from redis import asyncio as aioredis
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from src.core.config import test_settings
from src.db.base import Base
from src.db.database import get_db
from src.db.models.books import Author, Genre
from src.db.models.users import Role
from src.main import app
from src.schemas.author import AuthorResponse
from src.schemas.book import BookResponse
from src.schemas.genre import GenreResponse
from src.schemas.users import UserCreateResponseTest
from tests.utils import (
    create_author_for_tests,
    create_book_for_tests,
    create_genre_for_tests,
    create_user_for_tests,
)

fake = Faker()

DATABASE_URL_TEST: str = test_settings.database_url

engine_test = create_async_engine(DATABASE_URL_TEST, echo=False)
async_session_test = async_sessionmaker(
    bind=engine_test, expire_on_commit=False
)


async def override_get_db():
    async with async_session_test() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db  # type: ignore


@pytest.fixture(scope="function", autouse=True)
async def setup_test_db() -> AsyncGenerator[None, None]:
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield
    finally:
        async with engine_test.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine_test.dispose()


@pytest.fixture(scope="function", autouse=True)
async def initialize_cache() -> AsyncGenerator[None, None]:
    redis = aioredis.from_url(
        test_settings.REDIS_URL, encoding="utf8", decode_responses=True
    )
    await redis.ping()
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    await redis.aclose()


@pytest.fixture
async def async_client() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="function")
async def create_superuser() -> UserCreateResponseTest:
    async with async_session_test() as session:
        return await create_user_for_tests(
            session, "superuser@example.com", "Superuser1!", is_superuser=True
        )


@pytest.fixture(scope="function")
async def create_admin() -> UserCreateResponseTest:
    async with async_session_test() as session:
        return await create_user_for_tests(
            session, "administrator@example.com", "Administrator1!", Role.ADMIN
        )


@pytest.fixture(scope="function")
async def create_reader() -> UserCreateResponseTest:
    async with async_session_test() as session:
        return await create_user_for_tests(session, fake.email(), "Reader0!")


@pytest.fixture(scope="function")
async def create_three_readers() -> None:
    async with async_session_test() as session:
        for i in range(3):
            await create_user_for_tests(
                session, f"reader{i + 1}@example.com", f"Reader{i + 1}!"
            )


@pytest.fixture(scope="function")
async def create_author() -> AuthorResponse:
    async with async_session_test() as session:
        return await create_author_for_tests(
            session,
            "Some Author0",
            "2000-12-24",
            biography="author0 biography",
        )


@pytest.fixture(scope="function")
async def create_three_authors() -> None:
    async with async_session_test() as session:
        for i in range(3):
            await create_author_for_tests(
                session,
                f"Some Author{i + 1}",
                f"200{i + 1}-12-24",
                biography=f"author{i + 1} biography",
            )


@pytest.fixture(scope="function")
async def create_genre() -> GenreResponse:
    async with async_session_test() as session:
        return await create_genre_for_tests(session, "SomeGenre")


@pytest.fixture(scope="function")
async def create_book() -> BookResponse:
    async with async_session_test() as session:
        author = Author(
            id=1,
            name="SomeAuthor",
            biography="",
            birth_date=datetime.strptime("1890-12-24", "%Y-%m-%d").date(),
        )
        genre = Genre(
            name="SomeGenre",
        )
        return await create_book_for_tests(
            session,
            title="SomeGenre",
            published_at=f"2000-12-24",
            available_copies=1,
            authors=[author],
            genres=[genre],
        )


@pytest.fixture(scope="function")
async def create_three_books() -> None:
    async with async_session_test() as session:
        author = Author(
            id=1,
            name="SomeAuthor",
            biography="",
            birth_date=datetime.strptime("1890-12-24", "%Y-%m-%d").date(),
        )
        genre = Genre(
            name="SomeGenre",
        )
        for i in range(3):
            await create_book_for_tests(
                session,
                title=f"book{i + 1}@example.com",
                published_at=f"200{i + 1}-12-24",
                available_copies=i + 1,
                authors=[author],
                genres=[genre],
            )
