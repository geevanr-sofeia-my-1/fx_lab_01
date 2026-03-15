"""Minimal conservative execution engine."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from fxlab.domain.orders import Order
from fxlab.domain.trades import Trade
from fxlab.execution.costs import apply_exit_costs
from fxlab.execution.fills import next_bar_open_fill
from fxlab.execution.stops import stop_loss_touched
from fxlab.execution.targets import take_profit_touched
from fxlab.execution.tie_break import resolve_same_bar_exit


@dataclass(frozen=True)
class ExecutionConfigState:
    """Explicit execution assumptions for the minimal engine."""

    spread_pips: float
    slippage_pips: float
    same_bar_policy: str = "pessimistic"


def execute_long_only_strategy(
    rows: Sequence[dict[str, object]],
    *,
    spread_pips: float,
    slippage_pips: float,
) -> tuple[Trade, ...]:
    """Execute shifted long entry signals using next-bar-open fills.

    Expected row fields:
    - timestamp
    - open
    - high
    - low
    - close
    - entry_signal
    - stop_loss
    - take_profit
    """
    trades: list[Trade] = []
    open_order: Order | None = None
    entry_price: float | None = None
    entry_timestamp: str | None = None

    for index, row in enumerate(rows):
        if open_order is None and bool(row.get("entry_signal")):
            if index + 1 >= len(rows):
                break
            next_row = rows[index + 1]
            open_order = Order(
                timestamp=str(next_row["timestamp"]),
                side="long",
                stop_loss=float(row["stop_loss"]) if row.get("stop_loss") is not None else None,
                take_profit=(
                    float(row["take_profit"])
                    if row.get("take_profit") is not None
                    else None
                ),
                size=float(row.get("size", 1.0)),
            )
            entry_price = next_bar_open_fill(
                float(next_row["open"]),
                side="long",
                spread_pips=spread_pips,
                slippage_pips=slippage_pips,
            )
            entry_timestamp = str(next_row["timestamp"])
            continue

        if open_order is None or entry_price is None or entry_timestamp is None:
            continue

        low = float(row["low"])
        high = float(row["high"])
        stop_touched = stop_loss_touched(low, stop_loss=open_order.stop_loss)
        target_touched = take_profit_touched(high, take_profit=open_order.take_profit)
        exit_reason = resolve_same_bar_exit(
            stop_touched=stop_touched,
            target_touched=target_touched,
            policy="pessimistic",
        )

        if exit_reason is None:
            continue

        raw_exit = (
            open_order.stop_loss if exit_reason == "stop_loss" else open_order.take_profit
        )
        if raw_exit is None:
            continue
        exit_price = apply_exit_costs(raw_exit, side="long", slippage_pips=slippage_pips)
        pnl = (exit_price - entry_price) * open_order.size
        trades.append(
            Trade(
                entry_timestamp=entry_timestamp,
                exit_timestamp=str(row["timestamp"]),
                side="long",
                entry_price=entry_price,
                exit_price=exit_price,
                size=open_order.size,
                pnl=pnl,
                exit_reason=exit_reason,
            )
        )
        open_order = None
        entry_price = None
        entry_timestamp = None

    return tuple(trades)
