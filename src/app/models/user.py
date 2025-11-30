from datetime import datetime
from uuid import UUID

from .base_schema import BaseSchema


class User(BaseSchema):
    id: UUID
    email: str
    email_verified: bool = False
    username: str
    nickname: str
    discriminator: str
    created_date: datetime
    updated_date: datetime
    is_active: bool = True
