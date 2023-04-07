import os
from typing import Any, Callable

import alembic.command
import alembic.config

from personal_website.core.utils import parse_and_return_output

alembic_dir = os.path.dirname(os.path.abspath(__file__))


class AlembicHelper:
    def __init__(self, dsn: str, schema: str) -> None:
        self._config = alembic.config.Config(os.path.join(alembic_dir, "alembic.ini"))
        self._config.set_main_option("sqlalchemy.url", dsn)
        self._config.set_main_option("version_table_schema", schema)

    @parse_and_return_output
    def create_migration(self, message: str, autogenerate: bool = True) -> None:
        alembic.command.revision(
            self._config, message=message, autogenerate=autogenerate
        )

    @parse_and_return_output
    def upgrade_to_revision(self, revision: str, sql: bool = False) -> None:
        alembic.command.upgrade(self._config, revision=revision, sql=sql)

    @parse_and_return_output
    def downgrade_to_revision(self, revision: str) -> None:
        alembic.command.downgrade(self._config, revision=revision)

    @parse_and_return_output
    def set_revision(self, revision: str) -> None:
        alembic.command.upgrade(self._config, revision=revision)
        alembic.command.downgrade(self._config, revision=revision)
