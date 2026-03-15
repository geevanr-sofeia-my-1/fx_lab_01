"""Entry fill logic."""

from __future__ import annotations

from fxlab.execution.costs import apply_entry_costs


def next_bar_open_fill(
    next_bar_open: float,
    *,
    side: str,
    spread_pips: float,
    slippage_pips: float,
) -> float:
    """Fill a market order at the next bar open plus explicit costs."""
    return apply_entry_costs(
        next_bar_open,
        side=side,
        spread_pips=spread_pips,
        slippage_pips=slippage_pips,
    )
