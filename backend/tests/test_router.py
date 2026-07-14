from app.agents.router import route_by_category, route_after_grade


def test_route_by_category_maps_known_categories():
    assert route_by_category({"category": "order"}) == "order_search"
    assert route_by_category({"category": "shipping"}) == "shipping_search"
    assert route_by_category({"category": "general"}) == "general_search"


def test_route_by_category_defaults_to_general():
    assert route_by_category({"category": "unknown"}) == "general_search"
    assert route_by_category({}) == "general_search"


def test_route_after_grade_ends_when_grounded():
    assert route_after_grade({"grounded": True, "retries_exhausted": False, "category": "order"}) == "end"


def test_route_after_grade_retries_when_ungrounded_and_under_limit():
    assert route_after_grade({"grounded": False, "retries_exhausted": False, "category": "shipping"}) == "shipping_search"


def test_route_after_grade_ends_when_retries_exhausted():
    assert route_after_grade({"grounded": False, "retries_exhausted": True, "category": "general"}) == "end"
