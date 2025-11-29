from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse

from src.app.core.logger import get_logger, LoggingRoute
from ...models.base_schema import BaseSchema
from ...services.qr_service import QRService

_logger = get_logger(__name__)

router = APIRouter(
    prefix="/qr",
    tags=["QR Code"],
    route_class=LoggingRoute,
)


class QRRequestBody(BaseSchema):
    url: str = "https://resume.venibren.dev"
    background_color: str | None = None
    fill_color: str | None = None
    size: int = 10


@router.get(path="", response_class=StreamingResponse, status_code=status.HTTP_200_OK)
async def get_qr(
    url: str = "https://resume.venibren.dev",
    background_color: str | None = None,
    fill_color: str | None = None,
    size: int = 10,
) -> StreamingResponse:
    _logger.info("Generating QR code")

    _logger.silly(f"URL: {url}")
    _logger.silly(f"Background Color: {background_color}")
    _logger.silly(f"Fill Color: {fill_color}")
    _logger.silly(f"Size: {size}")

    qr_service = QRService()
    qr_service.generate(data=url)
    qr_service.add_watermark("./src/assets/qr_watermark.png")
    buffer = qr_service.to_buffer_stream()

    _logger.verbose("Returning StreamingResponse with QR code image")
    return StreamingResponse(buffer, media_type="image/png")


@router.post(path="", response_class=StreamingResponse, status_code=status.HTTP_200_OK)
async def post_qr(data: QRRequestBody) -> StreamingResponse:
    return await get_qr(
        url=data.url,
        background_color=data.background_color,
        fill_color=data.fill_color,
        size=data.size,
    )
