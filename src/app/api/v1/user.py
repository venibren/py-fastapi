from datetime import datetime
from fastapi import APIRouter
from uuid import UUID

from src.app.core.logger import get_logger, LoggingRoute

from ...models.user import User

_logger = get_logger(__name__)

router = APIRouter(prefix="/user", tags=["User"], route_class=LoggingRoute)


@router.get(path="")
@router.get(path="/{id}")
async def get_user(id: UUID) -> User:
    _logger.debug("ID: %s", id)

    user = User(
        id=id,
        email="brendan@venibren.dev",
        email_verified=True,
        username="venibren",
        nickname="Brendan",
        discriminator="0000",
        created_date=datetime.today(),
        updated_date=datetime.today(),
        is_active=True,
    )
    _logger.debug("User: %s", user)

    return user
