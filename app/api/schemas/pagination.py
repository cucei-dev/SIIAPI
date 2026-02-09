from pydantic import BaseModel
from typing import TypeVar, Generic

T = TypeVar('T')

class Pagination(BaseModel, Generic[T]):
    total: int
    results: list[T]
