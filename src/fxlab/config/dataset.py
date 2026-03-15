"""Dataset-related configuration models."""

from __future__ import annotations

from datetime import datetime

from pydantic import field_validator, model_validator

from fxlab.config.schema_base import FXLabBaseModel
from fxlab.domain.enums import Pair, PriceBasis, Timeframe


class DatasetRequestConfig(FXLabBaseModel):
    """Historical dataset request."""

    schema_version: str = "1"
    provider: str = "dukascopy"
    pair: Pair
    timeframe: Timeframe
    start: datetime
    end: datetime
    price_basis: PriceBasis

    @field_validator("provider")
    @classmethod
    def validate_provider(cls, value: str) -> str:
        if value != "dukascopy":
            raise ValueError("v1 provider must be dukascopy")
        return value

    @model_validator(mode="after")
    def validate_window(self) -> DatasetRequestConfig:
        if self.start.tzinfo is None or self.end.tzinfo is None:
            raise ValueError("start and end must be timezone-aware")
        if self.start >= self.end:
            raise ValueError("start must be earlier than end")
        return self
