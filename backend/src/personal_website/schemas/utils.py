from pydantic import BaseModel, Field


class TestMsg(BaseModel):
    result: str
