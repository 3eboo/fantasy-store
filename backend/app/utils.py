import json
import os
from typing import List
from .models import Product
from collections import defaultdict
from itertools import combinations, product



def load_products(path: str = None) -> List[Product]:
    if path is None:
        base_dir = os.path.dirname(__file__)
        path = os.path.join(base_dir, "data.json")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Product data file not found at: {path}")

    with open(path, "r") as f:
        data = json.load(f)

    return [Product(**item) for item in data]



def select_team(products: List[Product], budget: float) -> List[Product]:
    """
    Selects a team of 5 products from distinct categories that maximizes overall value
    while staying within a given budget. The algorithm balances product rating and
    total budget utilization to encourage thoughtful, cost-effective selection.

    Args:
        products (List[Product]): A list of available product entries.
        budget (float): The maximum total price for the team.

    Returns:
        List[Product]: A team of 5 products, each from a unique category.
    """

    # Group all eligible products by category (only rating >= 4.0)
    category_map = defaultdict(list)
    for p in products:
        if p.rating >= 4.0:
            category_map[p.category].append(p)

    # For each category, keep only the top 3 highest-value products
    # to reduce memory usage and computation time
    for cat in category_map:
        category_map[cat].sort(
            key=lambda p: (p.rating ** 2) / p.price, reverse=True
        )
        category_map[cat] = category_map[cat][:3]  # Trim to top 3

    best_team = []
    best_score = -1

    # Try all 5-category combinations
    for cat_combo in combinations(category_map.keys(), 5):
        # Generate all possible team combinations for this category combo
        for team in product(*(category_map[cat] for cat in cat_combo)):
            total_price = sum(p.price for p in team)
            if total_price > budget:
                continue  # skip if it exceeds the budget

            # Team value based on exponential rating (boosts high-rated products)
            team_rating_score = sum(p.rating ** 1.8 for p in team)

            # Reward teams that use more of the budget
            budget_util_score = 1 - (budget - total_price) / budget

            # Weighted total score (90% rating, 10% budget usage)
            total_score = team_rating_score * 0.9 + budget_util_score * 0.1

            if total_score > best_score:
                best_score = total_score
                best_team = team  # store best team found so far

    return list(best_team)
