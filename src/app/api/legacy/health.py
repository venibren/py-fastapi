from fastapi import APIRouter, Response, status

router = APIRouter(
    prefix="/health",
    tags=["Health Check"],
    responses={204: {"description": "No Content"}},
)


@router.get("/", status_code=status.HTTP_204_NO_CONTENT)
async def get_health() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)
