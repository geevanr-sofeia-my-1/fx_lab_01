"""Equity curve helpers."""

from __future__ import annotations

from collections.abc import Sequence

from fxlab.domain.account import AccountState


def equity_curve_from_account_states(states: Sequence[AccountState]) -> tuple[float, ...]:
    """Extract equity values from sequential account states."""
    return tuple(state.equity for state in states)
