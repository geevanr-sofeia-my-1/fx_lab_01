"""Risk configuration models."""

from __future__ import annotations

from pydantic import Field

from fxlab.config.schema_base import FXLabBaseModel


class RiskConfig(FXLabBaseModel):
    """Risk settings for baseline strategies."""

    schema_version: str = "1"
    starting_capital: float = Field(gt=0.0, default=500.0)
    risk_fraction: float = Field(gt=0.0, le=1.0, default=0.01)
    max_open_positions: int = Field(ge=1, default=1)
