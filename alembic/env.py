from logging.config import fileConfig

from alembic import context
from sqlalchemy import Connection, Inspector, inspect
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql.ddl import CreateSchema

from src.app.core.config import settings
from src.app.models import Base

import asyncio

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

_conn_str: str = f"postgresql+asyncpg://{settings.postgres_uri}"


def _include_name(name, type_, parent_names):
    if type_ == "schema":
        return name == settings.postgres_db_schema
    else:
        return True


def run_migrations_offline() -> None:
    context.configure(
        url=_conn_str,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # compare_type=True,
        # compare_server_default=True,
        include_schemas=True,
        # version_table="alembic_version",
        version_table_schema=settings.postgres_db_schema,
        include_name=_include_name,
    )
    with context.begin_transaction():
        context.run_migrations()


def _run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        # compare_type=True,
        # compare_server_default=True,
        include_schemas=True,
        # version_table="alembic_version",
        version_table_schema=settings.postgres_db_schema,
        include_name=_include_name,
    )

    inspector: Inspector = inspect(connection)
    if not inspector.has_schema(schema_name=settings.postgres_db_schema):
        connection.execute(CreateSchema(settings.postgres_db_schema))

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    engine = create_async_engine(_conn_str)
    async with engine.connect() as connection:
        await connection.run_sync(_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
