from fastapi import FastAPI, HTTPException, Query, Depends
from .models import ProductResponse
from .utils import load_products, select_team
from .deps import get_products
from typing import List
from .models import Product

from fastapi.middleware.cors import CORSMiddleware

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
    app.state.products = load_products()


@app.get("/team-builder", response_model=ProductResponse)
def team_builder(
        budget: float = Query(..., gt=0),
        products: List[Product] = Depends(get_products),
):
    team = select_team(products, budget)
    if len(team) < 5:
        raise HTTPException(status_code=400, detail="Not enough diverse products in budget")
    return {"products": team}
