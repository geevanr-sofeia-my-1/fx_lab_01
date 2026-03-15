"""Take-profit handling."""

from __future__ import annotations


def take_profit_touched(high: float, *, take_profit: float | None) -> bool:
    """Return whether a long take profit was touched within a bar."""
    return take_profit is not None and high >= take_profit
