from typing import Optional

from pydantic import AnyUrl, BaseModel, Field, constr


class CreateProductRequest(BaseModel):
    title: constr(strip_whitespace=True, min_length=1)
    price: float = Field(ge=0)
    description: constr(strip_whitespace=True, min_length=1)
    category: constr(strip_whitespace=True, min_length=1)
    image: AnyUrl


class ReplaceProductRequest(BaseModel):
    title: constr(strip_whitespace=True, min_length=1)
    price: float = Field(ge=0)
    description: constr(strip_whitespace=True, min_length=1)
    category: constr(strip_whitespace=True, min_length=1)
    image: AnyUrl


class PatchProductRequest(BaseModel):
    title: Optional[constr(strip_whitespace=True, min_length=1)] = None
    price: Optional[float] = Field(default=None, ge=0)
    description: Optional[constr(strip_whitespace=True, min_length=1)] = None
    category: Optional[constr(strip_whitespace=True, min_length=1)] = None
    image: Optional[AnyUrl] = None
