import io
import math

import qrcode
from PIL import Image


class QRService:
    # Initialize QR code with specified size and output format
    def __init__(self, size: int = 10) -> None:
        # Configure QR code parameters
        self.qr: qrcode.QRCode = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=size,
            border=math.ceil(size / 5),
        )

    # Generate QR code from URL
    def generate(self, url: str):
        # Add data to QR code
        self.qr.add_data(url)
        self.qr.make(fit=True)

        # Create QR code image
        self.qr_image = self.qr.make_image(
            back_color="#ffffff", fill_color="#000000"
        ).convert("RGBA")

    def add_watermark(self, logo_path: str):
        # Load and resize watermark image
        watermark: Image.Image = Image.open(logo_path).convert("RGBA")
        watermark_size: tuple[int, int] = (
            self.qr_image.size[0] // 4,
            self.qr_image.size[1] // 4,
        )
        watermark = watermark.resize(watermark_size, Image.Resampling.LANCZOS)
        watermark_mask: Image.Image = watermark.split()[3]

        # Calculate position to center the watermark
        position: tuple[int, int] = (
            (self.qr_image.size[0] - watermark.size[0]) // 2,
            (self.qr_image.size[1] - watermark.size[1]) // 2,
        )

        # Add white background for the watermark
        background = Image.new("RGBA", watermark.size, "#ffffff")
        self.qr_image.paste(background, position, background)

        # Paste watermark onto QR code image
        self.qr_image.paste(watermark, position, watermark_mask)

    def to_buffer_stream(self) -> io.BytesIO:
        # Create an in-memory bytes buffer
        buffer: io.BytesIO = io.BytesIO()

        # Save QR code image to the buffer
        self.qr_image.save(buffer, format="png")

        # Reset buffer's cursor to the beginning
        buffer.seek(0)

        return buffer
