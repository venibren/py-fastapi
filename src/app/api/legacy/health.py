from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix="/health",
    tags=["Health Check"],
    responses={204: {"healthy": True}},
)


@router.get("", response_class=bool)
async def get_health() -> bool:
    return True
