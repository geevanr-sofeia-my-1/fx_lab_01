"""Trade-level metrics."""

from __future__ import annotations

from collections.abc import Sequence

from fxlab.domain.trades import Trade


def win_rate(trades: Sequence[Trade]) -> float:
    """Return the fraction of winning trades."""
    if not trades:
        return 0.0
    wins = sum(trade.pnl > 0 for trade in trades)
    return wins / len(trades)


def expectancy(trades: Sequence[Trade]) -> float:
    """Return average PnL per trade."""
    if not trades:
        return 0.0
    return sum(trade.pnl for trade in trades) / len(trades)


def profit_factor(trades: Sequence[Trade]) -> float:
    """Return gross profit divided by gross loss magnitude."""
    gross_profit = sum(trade.pnl for trade in trades if trade.pnl > 0)
    gross_loss = -sum(trade.pnl for trade in trades if trade.pnl < 0)
    if gross_loss == 0:
        return float("inf") if gross_profit > 0 else 0.0
    return gross_profit / gross_loss
