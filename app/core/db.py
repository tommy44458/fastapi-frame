from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from config import SERVER_CONFIG
from core.base_model import Base


def _build_dsn() -> str:
    return (
        f"postgresql+asyncpg://{SERVER_CONFIG.DB_USER}:{SERVER_CONFIG.DB_PASSWORD}"
        f"@{SERVER_CONFIG.DB_HOST}:{SERVER_CONFIG.DB_PORT}/{SERVER_CONFIG.DB_NAME}"
    )


engine: AsyncEngine = create_async_engine(
    _build_dsn(),
    echo=False,
    pool_size=10,
    max_overflow=5,
    pool_recycle=300,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def init_db() -> None:
    """Dev-only helper: create all tables from metadata.

    For production use Alembic migrations instead.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def dispose_db() -> None:
    await engine.dispose()
