from typing import List

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware

from .deps import get_products
from .models import Product
from .models import ProductResponse
from .utils import load_products, select_team

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def load_product_data():
    """Initialize product data from file and store in app state."""
    app.state.products = load_products()


@app.get("/team-builder", response_model=ProductResponse)
def team_builder(
        budget: float = Query(..., gt=0),
        products: List[Product] = Depends(get_products),
) -> ProductResponse:
    """GET endpoint to return a value-optimized team of products within a budget.

    Args:
        budget (float): User-supplied budget to optimize within.

    Returns:
        ProductResponse: JSON payload with selected team.
    """
    team = select_team(products, budget)
    if len(team) < 5:
        raise HTTPException(status_code=400, detail="Not enough diverse products in budget")
    total_cost = round(sum(p.price for p in team), 2)
    return ProductResponse(products=team, total_cost=total_cost)
