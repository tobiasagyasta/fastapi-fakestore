from app.application.common.errors import NotFoundError
from app.application.common.pagination import PageMeta, PageResult
from app.domain.products.entity import Product

from .dto import CreateProductDTO, PatchProductDTO, ProductQuery, ReplaceProductDTO
from .ports import ProductRepository


class ListProductsUseCase:
    def __init__(self, repo: ProductRepository) -> None:
        self.repo = repo

    def execute(self, query: ProductQuery) -> PageResult[Product]:
        products, total = self.repo.list(query)
        pages = (total + query.limit - 1) // query.limit if query.limit > 0 else 0
        has_next = query.page < pages
        meta = PageMeta(
            page=query.page,
            limit=query.limit,
            total=total,
            pages=pages,
            has_next=has_next,
        )
        return PageResult(data=products, meta=meta)


class GetProductUseCase:
    def __init__(self, repo: ProductRepository) -> None:
        self.repo = repo

    def execute(self, product_id: int) -> Product:
        product = self.repo.get_by_id(product_id)
        if product is None:
            raise NotFoundError(f"Product {product_id} not found")
        return product


class ListCategoriesUseCase:
    def __init__(self, repo: ProductRepository) -> None:
        self.repo = repo

    def execute(self) -> list[str]:
        return self.repo.list_categories()


class CreateProductUseCase:
    def __init__(self, repo: ProductRepository) -> None:
        self.repo = repo

    def execute(self, data: CreateProductDTO) -> Product:
        return self.repo.create(data)


class ReplaceProductUseCase:
    def __init__(self, repo: ProductRepository) -> None:
        self.repo = repo

    def execute(self, product_id: int, data: ReplaceProductDTO) -> Product:
        return self.repo.replace(product_id, data)


class PatchProductUseCase:
    def __init__(self, repo: ProductRepository) -> None:
        self.repo = repo

    def execute(self, product_id: int, data: PatchProductDTO) -> Product:
        return self.repo.patch(product_id, data)


class DeleteProductUseCase:
    def __init__(self, repo: ProductRepository) -> None:
        self.repo = repo

    def execute(self, product_id: int) -> None:
        self.repo.delete(product_id)
