from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from ....services.qr_service import QRService

router = APIRouter(
    prefix="/qr",
    tags=["QR Code"],
)


@router.get("", response_class=StreamingResponse)
async def get_qr(
    url: str = "https://resume.venibren.dev",
    background_color: str | None = None,
    fill_color: str | None = None,
    size: int = 10,
) -> StreamingResponse:
    qr_service = QRService()
    qr_service.generate(data=url)

    qr_service.add_watermark("./src/assets/qr_watermark.png")

    buffer = qr_service.to_buffer_stream()

    return StreamingResponse(buffer, media_type="image/png")
