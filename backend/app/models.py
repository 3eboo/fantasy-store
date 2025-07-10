from typing import List

from pydantic import BaseModel


class Product(BaseModel):
    """Schema representing a product item."""
    id: int
    name: str
    category: str
    price: float
    rating: float


class ProductResponse(BaseModel):
    """Response schema containing selected team and total cost."""
    products: List[Product]
    total_cost: float

