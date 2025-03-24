from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import disconnect_db
from routers import health_router, texts_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on_startup

    yield

    # on_shutdown
    disconnect_db()


service = FastAPI(lifespan=lifespan)

service.include_router(health_router)
service.include_router(texts_router)
