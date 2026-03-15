"""Validation guard helpers."""

from __future__ import annotations

from collections.abc import Sequence


def meets_minimum_trade_count(trade_pnls: Sequence[float], *, minimum_trade_count: int) -> bool:
    """Return whether a result meets the required trade count threshold."""
    if minimum_trade_count <= 0:
        raise ValueError("minimum_trade_count must be positive")
    return len(trade_pnls) >= minimum_trade_count
