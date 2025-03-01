from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.config import test_settings
from src.db.base import Base

DATABASE_URL_TEST: str = test_settings.database_url

engine_test = create_async_engine(DATABASE_URL_TEST, echo=False)
async_session_test = async_sessionmaker(
    bind=engine_test, expire_on_commit=False
)


@pytest.fixture(scope="function")
async def setup_test_db() -> AsyncGenerator[None, None]:
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield
    finally:
        async with engine_test.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine_test.dispose()


@pytest.fixture(scope="function")
async def test_session(
    setup_test_db: None,
) -> AsyncGenerator[AsyncSession, None]:
    async with async_session_test() as session:
        yield session
