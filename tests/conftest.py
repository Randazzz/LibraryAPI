from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from src.core.config import test_settings
from src.db.base import Base
from src.db.database import get_db
from src.db.models.users import Role
from src.main import app
from src.schemas.users import UserCreateResponseTest
from tests.utils import create_user

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


@pytest.fixture
async def async_client() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="function")
async def create_superuser() -> UserCreateResponseTest:
    async with async_session_test() as session:
        return await create_user(
            session, "superuser@example.com", "Superuser1!", is_superuser=True
        )


@pytest.fixture(scope="function")
async def create_admin() -> UserCreateResponseTest:
    async with async_session_test() as session:
        return await create_user(
            session, "administrator@example.com", "Administrator1!", Role.ADMIN
        )


@pytest.fixture(scope="function")
async def create_reader() -> UserCreateResponseTest:
    async with async_session_test() as session:
        return await create_user(session, "reader0@example.com", "Reader0!")


@pytest.fixture(scope="function")
async def create_three_readers() -> None:
    async with async_session_test() as session:
        for i in range(3):
            await create_user(
                session, f"reader{i + 1}@example.com", f"Reader{i + 1}!"
            )
