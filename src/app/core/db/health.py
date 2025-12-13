from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.logger import get_logger

_logger = get_logger(__name__)


async def check_database_health(db: AsyncSession) -> bool:
    try:
        await db.execute(text("SELECT 1"))
        return True
    except Exception as ex:
        _logger.exception("Database health check failed: %s", ex)
        return False
