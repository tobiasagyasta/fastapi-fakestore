from fastapi import Depends

from app.application.products.use_cases import (
    CreateProductUseCase,
    DeleteProductUseCase,
    GetProductUseCase,
    ListCategoriesUseCase,
    ListProductsUseCase,
    PatchProductUseCase,
    ReplaceProductUseCase,
)
from app.infrastructure.db.repositories.product_repo_sql import SqlProductRepository
from app.infrastructure.db.session import get_db_session


def get_product_repo(
    session=Depends(get_db_session),
) -> SqlProductRepository:
    return SqlProductRepository(session)


def list_products_uc(
    repo: SqlProductRepository = Depends(get_product_repo),
) -> ListProductsUseCase:
    return ListProductsUseCase(repo)


def get_product_uc(
    repo: SqlProductRepository = Depends(get_product_repo),
) -> GetProductUseCase:
    return GetProductUseCase(repo)


def list_categories_uc(
    repo: SqlProductRepository = Depends(get_product_repo),
) -> ListCategoriesUseCase:
    return ListCategoriesUseCase(repo)


def create_product_uc(
    repo: SqlProductRepository = Depends(get_product_repo),
) -> CreateProductUseCase:
    return CreateProductUseCase(repo)


def replace_product_uc(
    repo: SqlProductRepository = Depends(get_product_repo),
) -> ReplaceProductUseCase:
    return ReplaceProductUseCase(repo)


def patch_product_uc(
    repo: SqlProductRepository = Depends(get_product_repo),
) -> PatchProductUseCase:
    return PatchProductUseCase(repo)


def delete_product_uc(
    repo: SqlProductRepository = Depends(get_product_repo),
) -> DeleteProductUseCase:
    return DeleteProductUseCase(repo)
