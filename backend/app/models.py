from pydantic import BaseModel
from typing import List


class Product(BaseModel):
    """Schema representing a product item."""
    id: int
    name: str
    category: str
    price: float
    rating: float


class ProductResponse(BaseModel):
    """Response schema containing selected team."""
    products: List[Product]
