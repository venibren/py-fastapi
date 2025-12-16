from sqlalchemy import MetaData
from sqlalchemy.dialects.postgresql import UUID as AlUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from uuid import UUID as PyUUID, uuid7

import re

from ..core.config import settings

_RE_1 = re.compile(r"(.)([A-Z][a-z]+)")
_RE_2 = re.compile(r"([a-z0-9])([A-Z])")


def to_snake_case(name: str) -> str:
    s1 = _RE_1.sub(r"\1_\2", name)
    return _RE_2.sub(r"\1_\2", s1).lower()


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        schema=settings.postgres_db_schema,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return to_snake_case(cls.__name__)

    id: Mapped[PyUUID] = mapped_column(
        AlUUID(as_uuid=True),
        primary_key=True,
        unique=True,
        default=uuid7,
        nullable=False,
    )

    pass
