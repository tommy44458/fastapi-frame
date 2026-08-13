from datetime import datetime
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from core.base_model import UUIDBase
from core.base_operator import UUIDOperator


class User(UUIDBase):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )


class UserOperator(UUIDOperator[User]):
    def __init__(self) -> None:
        super().__init__(User)

    async def get_by_username(self, session: AsyncSession, username: str) -> Optional[User]:
        result = await session.execute(
            select(User).where(User.username == username).limit(1)
        )
        return result.scalars().first()

    async def get_by_email(self, session: AsyncSession, email: str) -> Optional[User]:
        result = await session.execute(
            select(User).where(User.email == email).limit(1)
        )
        return result.scalars().first()


user_operator = UserOperator()
