from fastapi import APIRouter, Response, status

router = APIRouter(
    prefix="/health",
    tags=["Health"],
    responses={204: {"description": "No Content"}},
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
async def get_health() -> Response:
    """Health probe; returns 204 with an empty body."""
    return Response(status_code=status.HTTP_204_NO_CONTENT)
