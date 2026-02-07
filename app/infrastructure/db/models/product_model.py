from typing import Optional

from sqlmodel import Field, SQLModel


class ProductModel(SQLModel, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    price: float
    description: str
    category: str
    image: str
