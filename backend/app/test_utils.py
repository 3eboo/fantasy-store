from .utils import select_team, load_products


def test_team_selection():
    products = load_products()
    team = select_team(products, 500)
    assert len(team) == 5
    assert len(set(p.category for p in team)) == 5
    assert sum(p.price for p in team) <= 500
