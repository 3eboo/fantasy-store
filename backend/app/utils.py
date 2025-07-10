import json
import os
from typing import List
from .models import Product
from collections import defaultdict


def load_products(path: str = None) -> List[Product]:
    if path is None:
        base_dir = os.path.dirname(__file__)
        path = os.path.join(base_dir, "data.json")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Product data file not found at: {path}")

    with open(path, "r") as f:
        data = json.load(f)

    return [Product(**item) for item in data]


#  Goal
# We want a budget-sensitive, flexible team selection, that:
# Considers multiple product options per category
# Picks a combination of 5 distinct categories
# Maximizes value within the budget
# advantage: favours cheap + good rating  -> most probably static output, with good rated items

# def select_team(products: List[Product], budget: float) -> List[Product]:
#     from heapq import heappush, heappop
#
#     category_best = {}
#
#     for p in products:
#         if p.rating >= 4.0:
#             value_score = (p.rating ** 2) / p.price
#             if p.category not in category_best or value_score > category_best[p.category][0]:
#                 category_best[p.category] = (value_score, p)
#
#     # Create a sorted list by value descending
#     sorted_candidates = sorted(
#         [entry for entry in category_best.values()],
#         key=lambda x: x[0],
#         reverse=True
#     )
#
#     team = []
#     total_cost = 0.0
#
#     for _, product in sorted_candidates:
#         if len(team) >= 5:
#             break
#         if total_cost + product.price <= budget:
#             team.append(product)
#             total_cost += product.price
#
#     return team
#


# Here’s a more flexible approach:

# Group products by category
# For each category, sort products by a smart value metric
# Use a greedy selection to pick 5 products from different categories that best fit the budget


def select_team(products: List[Product], budget: float) -> List[Product]:
    from itertools import product, combinations

    # Group products by category, filter by rating
    category_map = defaultdict(list)
    for p in products:
        if p.rating >= 4.0:
            score = (p.rating ** 2) / p.price
            category_map[p.category].append((score, p))

    # Sort products in each category by value
    for cat in category_map:
        category_map[cat].sort(key=lambda x: x[0], reverse=True)

    # Pick top N candidates per category (to limit memory use)
    trimmed = {
        cat: [p for _, p in items[:3]]  # top 3 per category
        for cat, items in category_map.items()
    }

    # Try all 5-category combinations
    best_team = []
    best_value = 0

    category_combos = combinations(trimmed.keys(), 5)

    for cats in category_combos:
        for team in product(*(trimmed[c] for c in cats)):
            total_price = sum(p.price for p in team)
            if total_price <= budget:
                total_value = sum((p.rating ** 2) / p.price for p in team)
                if total_value > best_value:
                    best_team = team
                    best_value = total_value

    return list(best_team)
