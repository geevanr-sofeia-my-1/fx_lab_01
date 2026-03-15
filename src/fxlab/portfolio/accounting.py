"""Accounting helpers."""

from __future__ import annotations

from fxlab.domain.account import AccountState
from fxlab.domain.trades import Trade


def initialize_account(starting_cash: float) -> AccountState:
    """Initialize account state from starting cash."""
    if starting_cash <= 0:
        raise ValueError("starting_cash must be positive")
    return AccountState(cash=starting_cash, equity=starting_cash)


def apply_trade_to_account(account: AccountState, trade: Trade) -> AccountState:
    """Apply a realized trade to account cash and equity."""
    new_cash = account.cash + trade.pnl
    realized_pnl = account.realized_pnl + trade.pnl
    return AccountState(
        cash=new_cash,
        equity=new_cash,
        realized_pnl=realized_pnl,
        open_positions=account.open_positions,
    )
