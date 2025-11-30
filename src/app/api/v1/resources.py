import threading
import time
from fastapi import APIRouter, BackgroundTasks, Response, status

from src.app.core.logger import get_logger, LoggingRoute
from ...models.base_schema import BaseSchema

_logger = get_logger(__name__)

router = APIRouter(
    prefix="/resources",
    tags=["Recourses"],
    route_class=LoggingRoute,
)


@router.get(path="", status_code=status.HTTP_200_OK)
async def get_resources() -> Response:
    _logger.verbose("Resources endpoint hit")

    t = threading.Thread(target=background_task)
    t.start()

    return Response(
        content="Resources endpoint is working",
        media_type="text/plain",
        status_code=status.HTTP_200_OK,
    )


def background_task():
    _logger.info("Background task running")
    time.sleep(5)
    _logger.info("Background task completed")
