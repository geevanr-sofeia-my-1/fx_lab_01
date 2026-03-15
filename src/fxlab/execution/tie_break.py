"""Same-bar tie-break rules."""

from __future__ import annotations

from typing import Literal


def resolve_same_bar_exit(
    *,
    stop_touched: bool,
    target_touched: bool,
    policy: Literal["pessimistic"] = "pessimistic",
) -> Literal["stop_loss", "take_profit"] | None:
    """Resolve ambiguous same-bar stop/target touches."""
    if not stop_touched and not target_touched:
        return None
    if stop_touched and target_touched:
        if policy != "pessimistic":
            raise ValueError("unsupported tie-break policy")
        return "stop_loss"
    return "stop_loss" if stop_touched else "take_profit"
