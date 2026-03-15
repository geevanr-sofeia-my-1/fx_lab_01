"""Trade domain models."""

from __future__ import annotations

from typing import Literal

from fxlab.config.schema_base import FXLabBaseModel


class Trade(FXLabBaseModel):
    """Executed trade record."""

    entry_timestamp: str
    exit_timestamp: str
    side: Literal["long"]
    entry_price: float
    exit_price: float
    size: float
    pnl: float
    exit_reason: Literal["stop_loss", "take_profit", "time_exit"]
