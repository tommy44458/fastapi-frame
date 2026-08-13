from uuid import UUID, uuid4

from sqlalchemy import MetaData
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


NAMING_CONVENTION = {
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


class UUIDBase(Base):
    """Base for models keyed by a `uuid` primary key.

    Declaring the key here (rather than on each model) is what lets
    `UUIDOperator` be statically typed against the column it queries.
    """

    __abstract__ = True

    # sort_order keeps the key first in the emitted DDL. Without it, columns
    # inherited from an abstract base sort after the subclass's own columns,
    # which would silently reorder CREATE TABLE for every existing model.
    uuid: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4, sort_order=-1
    )


class IDBase(Base):
    """Base for models keyed by an autoincrementing integer `id` primary key."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, sort_order=-1)
