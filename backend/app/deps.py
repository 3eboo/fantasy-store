from fastapi import Request

from .models import Product


def get_products(request: Request) -> list[Product]:
    """FastAPI dependency to fetch product list from app state."""
    return request.app.state.products
