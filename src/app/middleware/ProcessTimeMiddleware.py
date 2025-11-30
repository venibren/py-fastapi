import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, app: ASGIApp, *, header_name: str = "x-process-time", precision: int = 4
    ) -> None:
        super().__init__(app)

        if precision < 0:
            raise ValueError("Precision must be greater than 0")

        self.header_name = header_name
        self.precision = precision

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.perf_counter()
        try:
            response = await call_next(request)
        finally:
            process_time = time.perf_counter() - start_time

        response.headers[self.header_name] = format(process_time, f".{self.precision}f")
        return response


__all__ = [ProcessTimeMiddleware]
