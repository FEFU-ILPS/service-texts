from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on_startup

    yield

    # on_shutdown


service = FastAPI(lifespan=lifespan)
