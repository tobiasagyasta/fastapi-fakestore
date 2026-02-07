from dataclasses import asdict
from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.application.common.errors import NotFoundError
from app.application.products.dto import (
    CreateProductDTO,
    PatchProductDTO,
    ProductQuery,
    ReplaceProductDTO,
)
from app.application.products.use_cases import (
    CreateProductUseCase,
    DeleteProductUseCase,
    GetProductUseCase,
    ListCategoriesUseCase,
    ListProductsUseCase,
    PatchProductUseCase,
    ReplaceProductUseCase,
)
from app.presentation.api.deps import (
    create_product_uc,
    delete_product_uc,
    get_product_uc,
    list_categories_uc,
    list_products_uc,
    patch_product_uc,
    replace_product_uc,
)
from app.presentation.api.mappers.product_mapper import product_to_response
from app.presentation.api.schemas.products import (
    CreateProductRequest,
    PatchProductRequest,
    ReplaceProductRequest,
)

router = APIRouter(prefix="/products", tags=["products"])


@router.get("")
def list_products(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    sort: Literal["asc", "desc"] = "asc",
    category: Optional[str] = None,
    q: Optional[str] = None,
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    use_case: ListProductsUseCase = Depends(list_products_uc),
) -> dict[str, object]:
    query = ProductQuery(
        page=page,
        limit=limit,
        sort=sort,
        category=category,
        q=q,
        min_price=min_price,
        max_price=max_price,
    )
    result = use_case.execute(query)
    return {
        "data": [product_to_response(product) for product in result.data],
        "meta": asdict(result.meta),
    }


@router.post("", status_code=201)
def create_product(
    payload: CreateProductRequest,
    use_case: CreateProductUseCase = Depends(create_product_uc),
) -> dict[str, object]:
    dto = CreateProductDTO(
        title=payload.title,
        price=payload.price,
        description=payload.description,
        category=payload.category,
        image=str(payload.image),
    )
    product = use_case.execute(dto)
    return product_to_response(product)


@router.put("/{product_id}")
def replace_product(
    product_id: int,
    payload: ReplaceProductRequest,
    use_case: ReplaceProductUseCase = Depends(replace_product_uc),
) -> dict[str, object]:
    dto = ReplaceProductDTO(
        title=payload.title,
        price=payload.price,
        description=payload.description,
        category=payload.category,
        image=str(payload.image),
    )
    try:
        product = use_case.execute(product_id, dto)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail="Product not found") from exc
    return product_to_response(product)


@router.patch("/{product_id}")
def patch_product(
    product_id: int,
    payload: PatchProductRequest,
    use_case: PatchProductUseCase = Depends(patch_product_uc),
) -> dict[str, object]:
    if all(
        value is None
        for value in [
            payload.title,
            payload.price,
            payload.description,
            payload.category,
            payload.image,
        ]
    ):
        raise HTTPException(status_code=400, detail="No fields to update")

    dto = PatchProductDTO(
        title=payload.title,
        price=payload.price,
        description=payload.description,
        category=payload.category,
        image=str(payload.image) if payload.image is not None else None,
    )
    try:
        product = use_case.execute(product_id, dto)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail="Product not found") from exc
    return product_to_response(product)


@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    use_case: DeleteProductUseCase = Depends(delete_product_uc),
) -> None:
    try:
        use_case.execute(product_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail="Product not found") from exc
    return None


@router.get("/categories")
def list_categories(
    use_case: ListCategoriesUseCase = Depends(list_categories_uc),
) -> list[str]:
    return use_case.execute()


@router.get("/{product_id}")
def get_product(
    product_id: int,
    use_case: GetProductUseCase = Depends(get_product_uc),
) -> dict[str, object]:
    try:
        product = use_case.execute(product_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return product_to_response(product)
