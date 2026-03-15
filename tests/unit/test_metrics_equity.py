"""Equity metric tests."""

from fxlab.metrics.equity import drawdown_series, max_drawdown, simple_return_series


def test_simple_return_series() -> None:
    assert simple_return_series((100.0, 110.0, 99.0)) == (0.1, -0.1)


def test_drawdown_series_and_max_drawdown() -> None:
    curve = (100.0, 110.0, 99.0, 120.0, 108.0)
    assert drawdown_series(curve) == (0.0, 0.0, -0.1, 0.0, -0.1)
    assert max_drawdown(curve) == -0.1
