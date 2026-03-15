"""Portfolio constraint helpers."""

from __future__ import annotations

from fxlab.domain.account import AccountState


def can_open_position(account: AccountState, *, max_open_positions: int) -> bool:
    """Return whether a new position may be opened."""
    if max_open_positions < 1:
        raise ValueError("max_open_positions must be at least 1")
    return account.open_positions < max_open_positions
