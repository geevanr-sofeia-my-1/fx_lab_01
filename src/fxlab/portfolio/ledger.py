"""Trade ledger helpers."""

from __future__ import annotations

from collections.abc import Sequence

from fxlab.domain.trades import Trade


def total_realized_pnl(trades: Sequence[Trade]) -> float:
    """Sum realized trade PnL."""
    return sum(trade.pnl for trade in trades)
