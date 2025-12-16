from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from uuid import UUID, uuid7

from src.app.core.logger import get_logger, LoggingRoute

from ...schemas.user import User, UserUpdate

_logger = get_logger(__name__)

router = APIRouter(prefix="/user", tags=["User"], route_class=LoggingRoute)


_user = User(
    id=uuid7(),
    email="brendan@venibren.dev",
    email_verified=True,
    username="venibren",
    nickname="Brendan",
    discriminator="0000",
    created_date=datetime.now(),
    updated_date=datetime.now(),
    is_active=True,
)


@router.get(
    path="/{id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
)
async def get_user(id: UUID) -> User:
    _logger.debug("Get user by id: %s", id)

    # if id != _user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    #     )

    return _user


@router.patch(
    path="/{id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
)
async def update_user(id: UUID, payload: UserUpdate) -> User:
    _logger.debug("Update user id: %s with payload: %s", id, payload.model_dump())

    if id != _user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    updated_fields = payload.model_dump(exclude_unset=True)

    for field, value in updated_fields.items():
        setattr(_user, field, value)

    _user.updated_date = datetime.now()

    return _user


@router.delete(
    path="/{id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
)
async def delete_user(id: UUID) -> User:
    _logger.debug("Delete user id: %s", id)

    if id != _user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    _user.email = f"deleted_{_user.email}"
    _user.is_active = False
    _user.updated_date = datetime.now()

    return _user
