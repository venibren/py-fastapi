from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

from ..config import settings


class Base(DeclarativeBase, MappedAsDataclass):
    pass


_conn_str: str = f"{settings.postgres_async_prefix}{settings.postgres_uri}"

async_engine: AsyncEngine = create_async_engine(_conn_str, echo=False, future=True, pool_pre_ping=True)

async_session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=async_engine,
    class_=AsyncSession,
)


async def async_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def dispose_engine() -> None:
    await async_engine.dispose()
