"""`users` schema 與主鍵 abstract base 的回歸測試。

主鍵宣告從 `User` 上移到 `UUIDBase` 之後,只有 `sort_order=-1` 在維持
`uuid` 仍是 DDL 的第一欄。拿掉它不會產生任何錯誤或型別問題 —— 只會讓
`CREATE TABLE` 悄悄改變欄位順序,所以這裡明確鎖住。
"""

from uuid import UUID

from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from core.base_model import Base, IDBase, UUIDBase
from models.user import User


EXPECTED_USER_COLUMNS = [
    "uuid",
    "username",
    "email",
    "password_hash",
    "is_active",
    "created_at",
    "updated_at",
]


class _IDProbe(IDBase):
    """只為了驗證 IDBase — repo 內目前沒有任何 model 使用整數主鍵。

    必須自帶一個非主鍵欄位,否則「id 在第一欄」的斷言在 IDBase 拿掉
    sort_order 後仍會通過(只有一欄時它必然是第一欄)。
    """

    __tablename__ = "_id_probe"

    label: Mapped[str] = mapped_column()


def test_users_column_order_keeps_primary_key_first() -> None:
    assert [c.name for c in User.__table__.columns] == EXPECTED_USER_COLUMNS


def test_users_primary_key_definition_is_preserved() -> None:
    uuid_col = User.__table__.c.uuid

    assert [c.name for c in User.__table__.primary_key.columns] == ["uuid"]
    assert isinstance(uuid_col.type, PG_UUID)
    assert uuid_col.type.as_uuid is True
    assert User.__table__.primary_key.name == "pk_users"

    # 斷言 default 真的會產生 UUID,而不是它包住哪個函式物件 ——
    # 後者依賴 SQLAlchemy 內部的包裝細節。
    assert uuid_col.default is not None
    assert isinstance(uuid_col.default.arg(None), UUID)


def test_id_base_puts_its_key_first_too() -> None:
    id_col = _IDProbe.__table__.c.id

    assert [c.name for c in _IDProbe.__table__.columns] == ["id", "label"]
    assert isinstance(id_col.type, Integer)
    assert id_col.primary_key is True


def test_abstract_bases_declare_no_tables_of_their_own() -> None:
    # 只斷言 abstract base 自己沒有建表,不去斷言整個 registry 有哪些表 ——
    # 後者會在每次新增 model 時假紅燈。
    assert not hasattr(UUIDBase, "__table__")
    assert not hasattr(IDBase, "__table__")
    assert {"uuidbase", "idbase"}.isdisjoint(Base.metadata.tables)
