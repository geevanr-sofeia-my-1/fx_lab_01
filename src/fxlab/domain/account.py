"""Account state domain models."""

from __future__ import annotations

from fxlab.config.schema_base import FXLabBaseModel


class AccountState(FXLabBaseModel):
    """Minimal account state."""

    cash: float
    equity: float
    realized_pnl: float = 0.0
    open_positions: int = 0
