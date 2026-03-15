"""Stop-loss handling."""

from __future__ import annotations


def stop_loss_touched(low: float, *, stop_loss: float | None) -> bool:
    """Return whether a long stop loss was touched within a bar."""
    return stop_loss is not None and low <= stop_loss
