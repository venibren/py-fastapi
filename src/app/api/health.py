from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.logger import get_logger, LoggingRoute
from src.app.core.db import async_get_db, check_database_health

_logger = get_logger(__name__)

router = APIRouter(
    prefix="/health",
    tags=["Health"],
    responses={204: {"description": "No Content"}},
    route_class=LoggingRoute,
)


@router.get(
    path="",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Health Check",
    description="Returns 204 No Content if the service is healthy.",
    operation_id="getHealth",
    responses={
        204: {"description": "Service is healthy"},
        503: {"description": "Service is not healthy"},
    },
)
async def get_health(db: AsyncSession = Depends(async_get_db)) -> Response:
    """Health probe; returns 204 with an empty body."""

    # db_alive = await check_database_health(db)
    # _logger.verbose("Database Alive: %s", db_alive)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
