"""Reproducibility and manifest domain models."""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import field_validator

from fxlab.config.schema_base import FXLabBaseModel
from fxlab.domain.enums import Pair, PriceBasis, Timeframe


class DatasetFingerprint(FXLabBaseModel):
    """Stable dataset identity information."""

    fingerprint: str
    pair: Pair
    timeframe: Timeframe
    provider: str
    price_basis: PriceBasis
    start: datetime
    end: datetime
    row_count: int
    preprocessing_version: str

    @field_validator("start", "end")
    @classmethod
    def validate_timestamps_are_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("timestamps must be timezone-aware")
        return value.astimezone(UTC)


class RunMetadata(FXLabBaseModel):
    """Experiment run reproducibility metadata."""

    run_id: str
    timestamp: datetime
    dataset_fingerprint: str
    strategy_config_hash: str
    validation_plan_id: str
    random_seed: int
    code_version: str | None = None

    @field_validator("timestamp")
    @classmethod
    def validate_timestamp(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("timestamp must be timezone-aware")
        return value.astimezone(UTC)
