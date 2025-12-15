from datetime import UTC, datetime
from enum import StrEnum
from sqlalchemy import DateTime, Enum, String
from sqlalchemy.dialects.postgresql import UUID as AlUUID
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from uuid import UUID as PyUUID, uuid8

from .base_model import BaseModel


class UserStatus(StrEnum):
    ACTIVE = "active"
    LOCKED = "locked"
    DISABLED = "disabled"
    PENDING_VERIFICATION = "pending_verification"


class User(BaseModel):
    __tablename__ = "Users"

    id: Mapped[PyUUID] = mapped_column(
        AlUUID(as_uuid=True),
        primary_key=True,
        unique=True,
        default_factory=uuid8,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    email_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    email_verified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
    )
    status = Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, name="user_status", native_enum=True),
        default=UserStatus.PENDING_VERIFICATION,
        nullable=False,
    )
