from typing import Generic, Optional, Sequence, Type, TypeVar
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.base_model import Base


ModelT = TypeVar("ModelT", bound=Base)


class BaseOperator(Generic[ModelT]):
    """Async-only repository for CRUD on a SQLAlchemy model.

    Subclasses bind a concrete model class and may add domain-specific queries.
    """

    def __init__(self, model: Type[ModelT]):
        self.model = model

    async def create(self, session: AsyncSession, instance: ModelT) -> ModelT:
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    async def get_all(self, session: AsyncSession) -> Sequence[ModelT]:
        result = await session.execute(select(self.model))
        return result.scalars().all()


class UUIDOperator(BaseOperator[ModelT]):
    """Repository for models keyed by `uuid` column."""

    async def get(self, session: AsyncSession, uuid: UUID | str) -> Optional[ModelT]:
        result = await session.execute(
            select(self.model).where(self.model.uuid == uuid).limit(1)
        )
        return result.scalars().first()

    async def update(self, session: AsyncSession, uuid: UUID | str, data: dict) -> None:
        await session.execute(
            update(self.model).where(self.model.uuid == uuid).values(data)
        )
        await session.commit()

    async def delete(self, session: AsyncSession, uuid: UUID | str) -> None:
        await session.execute(delete(self.model).where(self.model.uuid == uuid))
        await session.commit()


class IDOperator(BaseOperator[ModelT]):
    """Repository for models keyed by integer `id` column."""

    async def get(self, session: AsyncSession, id_: int) -> Optional[ModelT]:
        result = await session.execute(
            select(self.model).where(self.model.id == id_).limit(1)
        )
        return result.scalars().first()

    async def update(self, session: AsyncSession, id_: int, data: dict) -> None:
        await session.execute(
            update(self.model).where(self.model.id == id_).values(data)
        )
        await session.commit()

    async def delete(self, session: AsyncSession, id_: int) -> None:
        await session.execute(delete(self.model).where(self.model.id == id_))
        await session.commit()
