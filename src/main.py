import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import RedisError
from redis import asyncio as aioredis

from src.api.v1 import router as v1_router
from src.core.config import settings
from src.core.logging import setup_logging

setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    try:
        redis = aioredis.from_url(
            settings.REDIS_URL, encoding="utf8", decode_responses=True
        )
        await redis.ping()
        logger.info("Successfully connected to Redis!")
    except RedisError as e:
        logger.error(
            f"Failed to connect to Redis: {type(e).__name__}: {str(e)}"
        )
        raise RuntimeError(f"Redis connection error: {e}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    await redis.aclose()


app = FastAPI(debug=settings.DEBUG, lifespan=lifespan)

app.include_router(v1_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
