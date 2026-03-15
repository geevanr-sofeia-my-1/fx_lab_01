"""Execution cost helpers."""

from __future__ import annotations


def apply_entry_costs(
    price: float,
    *,
    side: str,
    spread_pips: float,
    slippage_pips: float,
) -> float:
    """Apply conservative costs to an entry fill."""
    if side != "long":
        raise ValueError("only long side is supported in the current execution slice")
    return price + spread_pips + slippage_pips


def apply_exit_costs(price: float, *, side: str, slippage_pips: float) -> float:
    """Apply conservative costs to an exit fill."""
    if side != "long":
        raise ValueError("only long side is supported in the current execution slice")
    return price - slippage_pips
