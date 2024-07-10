import logging
from contextlib import asynccontextmanager
from typing import Any

import uvicorn

from fastapi import FastAPI, Depends

from fastapi_limiter import FastAPILimiter
from redis.asyncio import Redis

from src.cache import redis
from src.configs import settings, LOGGING

from src.endpoints.v1 import (
    tokens,
    users,
    users_additional,
)
from src.services.start_up import StartUpService
from src.db.clients.postgres import get_postgres_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    startup_methods: StartUpService = StartUpService(
        database=Depends(get_postgres_db), settings=settings.start_up
    )
    await startup_methods.create_admin_user()
    redis.redis = redis.RedisCache(
        Redis(**settings.redis.connection_dict), settings=settings.token
    )
    await FastAPILimiter.init(Redis(**settings.redis.connection_dict))
    yield
    await redis.redis.close()
    await FastAPILimiter.close()


app = FastAPI(
    title=settings.app.name,
    description=settings.app.description,
    docs_url=settings.app.docs_url,
    openapi_url=settings.app.openapi_url,
    lifespan=lifespan,
)

include_router(
    users.router,
    prefix="/auth/v1/users",
    tags=["users"],
)
app.include_router(
    users_additional.router, prefix="/auth/v1/users", tags=["users_additional"]
)
app.include_router(tokens.router, prefix="/auth/v1/tokens", tags=["tokens"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.app.host,
        port=settings.app.port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
