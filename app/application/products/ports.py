from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.products.entity import Product

from .dto import CreateProductDTO, PatchProductDTO, ProductQuery, ReplaceProductDTO


class ProductRepository(ABC):
    @abstractmethod
    def list(self, query: ProductQuery) -> tuple[list[Product], int]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, product_id: int) -> Product | None:
        raise NotImplementedError

    @abstractmethod
    def list_categories(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def create(self, data: CreateProductDTO) -> Product:
        raise NotImplementedError

    @abstractmethod
    def replace(self, product_id: int, data: ReplaceProductDTO) -> Product:
        raise NotImplementedError

    @abstractmethod
    def patch(self, product_id: int, data: PatchProductDTO) -> Product:
        raise NotImplementedError

    @abstractmethod
    def delete(self, product_id: int) -> None:
        raise NotImplementedError
