import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool, text
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from personal_website.core.config import Config
from personal_website.db.dbhelper import DBHelper
from personal_website.db.orm.base import Base
from personal_website.db.orm.common import Company, WorkExperience

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_dbhelper() -> DBHelper:
    db_conn_config = Config.instance.db_conn
    return DBHelper(
        sqlalchemy_async_database_uri=db_conn_config.sqlalchemy_async_database_uri,
        dbschema=db_conn_config.dbschema,
        pool_size=1,
        echo=True,
    )


def get_migrations_sql() -> None:
    dbhelper = get_dbhelper()
    engine = dbhelper.async_engine
    context.configure(
        url=engine.url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema=dbhelper.dbschema,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    dbhelper = get_dbhelper()
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        version_table_schema=dbhelper.dbschema,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    async_engine = get_dbhelper().async_engine

    async with async_engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await async_engine.dispose()


def run_migrations() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    get_migrations_sql()
else:
    run_migrations()
