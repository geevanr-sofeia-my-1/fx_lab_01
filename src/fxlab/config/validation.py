"""Validation plan configuration models."""

from __future__ import annotations

from pydantic import Field

from fxlab.config.schema_base import FXLabBaseModel


class ValidationPlanConfig(FXLabBaseModel):
    """Validation split and walk-forward settings."""

    schema_version: str = "1"
    train_fraction: float = Field(gt=0.0, lt=1.0, default=0.6)
    validation_fraction: float = Field(gt=0.0, lt=1.0, default=0.2)
    test_fraction: float = Field(gt=0.0, lt=1.0, default=0.2)
    minimum_trade_count: int = Field(ge=1, default=30)
