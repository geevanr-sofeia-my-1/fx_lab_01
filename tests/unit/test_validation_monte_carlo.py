"""Monte Carlo validation tests."""

from fxlab.validation.guards import meets_minimum_trade_count
from fxlab.validation.monte_carlo import monte_carlo_trade_pnl


def test_monte_carlo_trade_pnl_is_deterministic_under_fixed_seed() -> None:
    left = monte_carlo_trade_pnl((1.0, -1.0, 2.0), seed=7, iterations=3)
    right = monte_carlo_trade_pnl((1.0, -1.0, 2.0), seed=7, iterations=3)
    assert left == right


def test_meets_minimum_trade_count() -> None:
    assert meets_minimum_trade_count((1.0, 2.0, 3.0), minimum_trade_count=3) is True
    assert meets_minimum_trade_count((1.0, 2.0), minimum_trade_count=3) is False
