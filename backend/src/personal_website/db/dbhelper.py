import json
from typing import Any

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from personal_website.alembic.migrations import AlembicHelper


class DBHelper:
    def __init__(
        self,
        sqlalchemy_async_database_uri: str,
        dbschema: str,
        poolclass: type[sa.pool.Pool] = sa.pool.AsyncAdaptedQueuePool,
        **engine_kwargs: Any,
    ) -> None:
        self.dbschema = dbschema
        self.async_engine = create_async_engine(
            sqlalchemy_async_database_uri,
            json_serializer=json.dumps,
            json_deserializer=json.loads,
            poolclass=poolclass,
        )
        self.async_engine.update_execution_options(
            schema_translate_map={None: self.dbschema}
        )
        self.create_async_session = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.async_engine,
            class_=AsyncSession,
        )
