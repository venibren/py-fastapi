from fastapi import Request
from fastapi.responses import Response
from fastapi.routing import APIRoute
import logging
import logging.config
import time

from src.app.core.config import settings

# Custom log levels
SILLY_LEVEL = 5
VERBOSE_LEVEL = 15
logging.addLevelName(SILLY_LEVEL, "SILLY")
logging.addLevelName(VERBOSE_LEVEL, "VERBOSE")


# Extend Logger class with custom methods
def _silly(self: logging.Logger, msg, *args, **kwargs) -> None:
    if self.isEnabledFor(SILLY_LEVEL):
        self._log(SILLY_LEVEL, msg, args, **kwargs)


# Extend Logger class with custom methods
def _verbose(self: logging.Logger, msg, *args, **kwargs) -> None:
    if self.isEnabledFor(VERBOSE_LEVEL):
        self._log(VERBOSE_LEVEL, msg, args, **kwargs)


# Attach methods to Logger class
logging.Logger.silly = _silly
logging.Logger.verbose = _verbose


# Setup logger configuration
def setup_logger() -> logging.Logger:
    """Setup logging configuration with colorful output using RichHandler."""

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"rich": {"format": "%(message)s"}},
        "handlers": {
            "console": {
                "class": "rich.logging.RichHandler",
                "level": settings.log_level,
                "formatter": "rich",
                "rich_tracebacks": True,
                "markup": True,
                "show_time": True,
                "show_level": True,
                "show_path": True,
                "enable_link_path": True,
                "log_time_format": "%Y-%m-%d %H:%M:%S.%f",
            }
        },
        "root": {"level": settings.log_level, "handlers": ["console"]},
    }

    logging.config.dictConfig(config)

    for n in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        lg = logging.getLogger(n)
        lg.propagate = False
        lg.handlers = []

    logger = logging.getLogger(settings.app_name)
    logger.verbose("Logging initialized at level=%s", settings.log_level)

    return logger


# Get logger by name
def get_logger(name: str) -> logging.Logger:
    """Get a logger by name."""

    return logging.getLogger(name)


# Auto-logging route class
class LoggingRoute(APIRoute):
    """Auto-log each endpoint invocation."""

    def get_route_handler(self):
        original_handler = super().get_route_handler()

        async def handler(request: Request) -> Response:
            logger = get_logger(settings.app_name)
            route_name = (
                getattr(request.scope.get("route"), "name", None)
                or self.name
                or "unknown"
            )
            method = request.method
            path = request.url.path

            # Endpoint triggered
            logger.info("HTTP %s %s -> %s", method, path, route_name)

            start = time.perf_counter()
            try:
                response: Response = await original_handler(request)
            except Exception:
                # Keep errors visible with traceback
                logger.exception("Unhandled exception in %s %s", method, path)
                raise
            finally:
                elapsed_ms = (time.perf_counter() - start) * 1000.0

            # Completion details
            try:
                status_code = getattr(response, "status_code", "n/a")
            except Exception:
                status_code = "n/a"
            logger.info(
                "Completed %s %s -> %s in %.2f ms",
                method,
                path,
                status_code,
                elapsed_ms,
            )
            return response

        return handler


__all__ = ["get_logger", "setup_logger", "LoggingRoute"]
