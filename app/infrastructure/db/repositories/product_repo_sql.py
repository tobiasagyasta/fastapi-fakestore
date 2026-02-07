from __future__ import annotations

from typing import cast

from sqlalchemy import asc, desc, func, or_
from sqlalchemy.sql.elements import ColumnElement
from sqlmodel import Session, select

from app.application.common.errors import NotFoundError
from app.application.products.dto import (
    CreateProductDTO,
    PatchProductDTO,
    ProductQuery,
    ReplaceProductDTO,
)
from app.application.products.ports import ProductRepository
from app.domain.products.entity import Product
from app.infrastructure.db.models.product_model import ProductModel


def _to_domain(model: ProductModel) -> Product:
    return Product(
        id=model.id or 0,
        title=model.title,
        price=model.price,
        description=model.description,
        category=model.category,
        image=model.image,
    )


class SqlProductRepository(ProductRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self, query: ProductQuery) -> tuple[list[Product], int]:
        conditions: list[ColumnElement[bool]] = []

        if query.category:
            conditions.append(ProductModel.category == query.category)

        if query.q:
            pattern = f"%{query.q}%"
            title_match = func.lower(ProductModel.title).like(func.lower(pattern))
            desc_match = func.lower(ProductModel.description).like(func.lower(pattern))
            conditions.append(or_(title_match, desc_match))

        if query.min_price is not None:
            conditions.append(ProductModel.price >= query.min_price)

        if query.max_price is not None:
            conditions.append(ProductModel.price <= query.max_price)

        stmt = select(ProductModel)
        if conditions:
            stmt = stmt.where(*conditions)

        order_by = asc(ProductModel.id) if query.sort == "asc" else desc(ProductModel.id)
        stmt = (
            stmt.order_by(order_by)
            .offset((query.page - 1) * query.limit)
            .limit(query.limit)
        )
        models = self.session.exec(stmt).all()

        count_stmt = select(func.count()).select_from(ProductModel)
        if conditions:
            count_stmt = count_stmt.where(*conditions)
        total = cast(int, self.session.exec(count_stmt).one())

        return ([_to_domain(model) for model in models], int(total))

    def get_by_id(self, product_id: int) -> Product | None:
        model = self.session.get(ProductModel, product_id)
        if model is None:
            return None
        return _to_domain(model)

    def list_categories(self) -> list[str]:
        stmt = select(ProductModel.category).distinct().order_by(ProductModel.category.asc())
        categories = self.session.exec(stmt).all()
        return list(categories)

    def create(self, data: CreateProductDTO) -> Product:
        model = ProductModel(
            title=data.title,
            price=data.price,
            description=data.description,
            category=data.category,
            image=data.image,
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return _to_domain(model)

    def replace(self, product_id: int, data: ReplaceProductDTO) -> Product:
        model = self.session.get(ProductModel, product_id)
        if model is None:
            raise NotFoundError("Product not found")

        model.title = data.title
        model.price = data.price
        model.description = data.description
        model.category = data.category
        model.image = data.image

        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return _to_domain(model)

    def patch(self, product_id: int, data: PatchProductDTO) -> Product:
        model = self.session.get(ProductModel, product_id)
        if model is None:
            raise NotFoundError("Product not found")

        if data.title is not None:
            model.title = data.title
        if data.price is not None:
            model.price = data.price
        if data.description is not None:
            model.description = data.description
        if data.category is not None:
            model.category = data.category
        if data.image is not None:
            model.image = data.image

        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return _to_domain(model)

    def delete(self, product_id: int) -> None:
        model = self.session.get(ProductModel, product_id)
        if model is None:
            raise NotFoundError("Product not found")
        self.session.delete(model)
        self.session.commit()
