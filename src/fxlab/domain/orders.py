"""Order domain models."""

from __future__ import annotations

from typing import Literal

from fxlab.config.schema_base import FXLabBaseModel


class Order(FXLabBaseModel):
    """Minimal market entry order."""

    timestamp: str
    side: Literal["long"]
    stop_loss: float | None = None
    take_profit: float | None = None
    size: float = 1.0
