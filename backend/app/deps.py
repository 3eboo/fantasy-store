from fastapi import Request
from .models import Product


def get_products(request: Request) -> list[Product]:
    return request.app.state.products
