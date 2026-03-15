"""Canonical bar schema."""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import field_validator, model_validator

from fxlab.config.schema_base import FXLabBaseModel
from fxlab.domain.enums import Pair, PriceBasis, Timeframe


class CanonicalBar(FXLabBaseModel):
    """Canonical OHLCV record."""

    pair: Pair
    timeframe: Timeframe
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float | None = None
    tick_volume: float | None = None
    spread: float | None = None
    source: str
    provider: str = "dukascopy"
    source_instrument: str | None = None
    price_basis: PriceBasis
    is_complete_bar: bool = True
    session_asia: bool = False
    session_london: bool = False
    session_newyork: bool = False

    @field_validator("timestamp")
    @classmethod
    def validate_timestamp_is_utc(cls, value: datetime) -> datetime:
        """Require timezone-aware UTC timestamps."""
        if value.tzinfo is None:
            raise ValueError("timestamp must be timezone-aware")
        normalized = value.astimezone(UTC)
        if normalized.utcoffset() != UTC.utcoffset(normalized):
            raise ValueError("timestamp must normalize to UTC")
        return normalized

    @model_validator(mode="after")
    def validate_ohlc(self) -> CanonicalBar:
        """Validate OHLC ordering and non-negative numeric fields."""
        if min(self.open, self.high, self.low, self.close) <= 0:
            raise ValueError("prices must be positive")
        if self.high < max(self.open, self.close):
            raise ValueError("high must be at least max(open, close)")
        if self.low > min(self.open, self.close):
            raise ValueError("low must be at most min(open, close)")
        if self.low > self.high:
            raise ValueError("low cannot exceed high")
        for field_name in ("volume", "tick_volume", "spread"):
            value = getattr(self, field_name)
            if value is not None and value < 0:
                raise ValueError(f"{field_name} cannot be negative")
        return self
