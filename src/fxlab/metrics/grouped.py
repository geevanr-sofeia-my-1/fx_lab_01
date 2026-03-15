"""Grouped metrics helpers."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence

from fxlab.domain.trades import Trade


def group_trades_by_exit_reason(trades: Sequence[Trade]) -> dict[str, tuple[Trade, ...]]:
    """Group trades by exit reason."""
    grouped: dict[str, list[Trade]] = defaultdict(list)
    for trade in trades:
        grouped[trade.exit_reason].append(trade)
    return {key: tuple(value) for key, value in grouped.items()}
