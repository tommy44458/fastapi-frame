from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routers.auth import router as auth_router
from api.routers.health import router as health_router
from config import APP_VERSION, SERVER_CONFIG
from core.db import dispose_db, init_db
from core.logging import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    if SERVER_CONFIG.AUTO_CREATE_TABLES:
        await init_db()
    yield
    await dispose_db()


def create_app() -> FastAPI:
    app = FastAPI(
        title=SERVER_CONFIG.APP_NAME,
        version=APP_VERSION,
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=SERVER_CONFIG.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health_router)
    app.include_router(auth_router)
    return app


app = create_app()
