"""Equity and drawdown metrics."""

from __future__ import annotations

from collections.abc import Sequence


def simple_return_series(equity_curve: Sequence[float]) -> tuple[float, ...]:
    """Return simple period-over-period returns."""
    if len(equity_curve) < 2:
        return ()
    returns: list[float] = []
    for previous, current in zip(equity_curve[:-1], equity_curve[1:], strict=False):
        if previous == 0:
            raise ValueError("equity curve contains zero, cannot compute simple returns")
        returns.append((current - previous) / previous)
    return tuple(returns)


def drawdown_series(equity_curve: Sequence[float]) -> tuple[float, ...]:
    """Return drawdown percentages from running peak."""
    if not equity_curve:
        return ()
    peak = equity_curve[0]
    drawdowns: list[float] = []
    for value in equity_curve:
        peak = max(peak, value)
        drawdowns.append(0.0 if peak == 0 else (value - peak) / peak)
    return tuple(drawdowns)


def max_drawdown(equity_curve: Sequence[float]) -> float:
    """Return the most negative drawdown."""
    series = drawdown_series(equity_curve)
    return min(series) if series else 0.0
