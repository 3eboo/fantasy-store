from pydantic import BaseModel
from typing import List


class Product(BaseModel):
    id: int
    name: str
    category: str
    price: float
    rating: float


class ProductResponse(BaseModel):
    products: List[Product]
