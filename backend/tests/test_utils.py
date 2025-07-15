from backend.app.models import Product
from backend.app.utils import select_team

# Sample mock data with multiple categories and valid ratings
mock_products = [
    Product(id=1, name="A", category="Cat1", price=50, rating=4.5),
    Product(id=2, name="B", category="Cat2", price=40, rating=4.2),
    Product(id=3, name="C", category="Cat3", price=60, rating=4.8),
    Product(id=4, name="D", category="Cat4", price=30, rating=4.1),
    Product(id=5, name="E", category="Cat5", price=70, rating=4.6),
    Product(id=6, name="F", category="Cat1", price=55, rating=4.3),  # Duplicate category
]


def test_select_team_returns_five_unique_categories():
    team = select_team(mock_products, budget=300)
    assert len(team) == 5, "Team should have 5 products"
    assert len(set(p.category for p in team)) == 5, "Each product should have a unique category"


def test_select_team_respects_budget():
    team = select_team(mock_products, budget=250)
    total_price = sum(p.price for p in team)
    assert total_price <= 250, f"Total price {total_price} should be under budget"


def test_select_team_empty_if_budget_too_low():
    team = select_team(mock_products, budget=50)
    assert isinstance(team, list), "Should return a list"
    assert len(team) < 5, "Should return less than 5 if budget is insufficient"
