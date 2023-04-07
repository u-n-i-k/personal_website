import json
import re
from typing import Any

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Json(sa.TypeDecorator):
    impl = sa.JSON

    cache_ok = True

    def coerce_compared_value(
        self, op: sa.sql.operators.OperatorType | None, value: Any
    ) -> Any:
        return self.impl.coerce_compared_value(op, value)  # type: ignore

    def process_literal_param(value: Any, dialect: sa.engine.Dialect) -> str:  # type: ignore
        if value is None:
            return "null"
        return "'" + json.dumps(value).replace("'", "\\'") + "'"


class Base(DeclarativeBase):
    _repr_attrs: list[str] = []

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()

    @property
    def session(self) -> AsyncSession | None:
        return AsyncSession.object_session(self)  # type: ignore

    async def lock(self, with_for_update: Any = False) -> None:
        if self.session is not None:
            await self.session.refresh(self, with_for_update=with_for_update)

    def update(self, obj_in: BaseModel) -> None:
        raise NotImplementedError

    def __repr__(self) -> str:
        fields = ", ".join(
            [
                f"{attr_name}={str(getattr(self, attr_name, ''))}"
                for attr_name in self._repr_attrs
            ]
        )
        return f"{self.__class__.__name__}({fields})"
