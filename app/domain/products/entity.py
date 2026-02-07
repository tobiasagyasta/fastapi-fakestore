from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    id: int
    title: str
    price: float
    description: str
    category: str
    image: str
