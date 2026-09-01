from app.services.metrics import calculate_rate


def test_calculate_rate_returns_percentage() -> None:
    assert calculate_rate(25, 1000) == 2.5


def test_calculate_rate_returns_zero_when_impressions_are_zero() -> None:
    assert calculate_rate(10, 0) == 0.0
