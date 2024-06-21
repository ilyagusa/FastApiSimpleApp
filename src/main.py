from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from redis import asyncio as aioredis
from fastapi import FastAPI, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.staticfiles import StaticFiles

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate
from operations.router import router as router_operations
from tasks.router import router as router_tasks
from pages.router import router as router_pages
from chat.router import router as router_chat

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(router_operations)
app.include_router(router_tasks)
app.include_router(router_pages)
app.include_router(router_chat)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost:6379")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
