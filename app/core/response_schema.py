from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class IResponse(BaseModel, Generic[T]):
    detail: str
    status_code: int
    ok: bool = True
    data: T | None = None
    page: int | None = None
    offset: int | None = None
