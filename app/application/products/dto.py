from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ProductQuery:
    page: int = 1
    limit: int = 10
    sort: str = "asc"
    category: Optional[str] = None
    q: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None


@dataclass(frozen=True)
class CreateProductDTO:
    title: str
    price: float
    description: str
    category: str
    image: str


@dataclass(frozen=True)
class ReplaceProductDTO:
    title: str
    price: float
    description: str
    category: str
    image: str


@dataclass(frozen=True)
class PatchProductDTO:
    title: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    category: Optional[str] = None
    image: Optional[str] = None
