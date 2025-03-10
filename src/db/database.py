import logging
from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.config import settings
from src.core.exceptions import DatabaseConnectionException

logger = logging.getLogger(__name__)

engine = create_async_engine(settings.database_url, echo=settings.DEBUG)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            logger.error(f"Ошибка подключения к базе данных: {e}")
            raise DatabaseConnectionException()
