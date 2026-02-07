from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class PageMeta:
    page: int
    limit: int
    total: int
    pages: int
    has_next: bool


@dataclass(frozen=True)
class PageResult(Generic[T]):
    data: list[T]
    meta: PageMeta
