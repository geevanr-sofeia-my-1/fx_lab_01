"""Internal historical data provider contracts."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import UTC, datetime
from pathlib import Path

from pydantic import Field, field_validator, model_validator

from fxlab.config.schema_base import FXLabBaseModel
from fxlab.domain.enums import Pair, PriceBasis, Timeframe


class ProviderRequest(FXLabBaseModel):
    """Internal normalized provider request."""

    pair: Pair
    timeframe: Timeframe
    start: datetime
    end: datetime
    price_basis: PriceBasis
    chunk_size_days: int | None = Field(default=None, ge=1)

    @field_validator("start", "end")
    @classmethod
    def validate_timestamp(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("provider request timestamps must be timezone-aware")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def validate_range(self) -> ProviderRequest:
        if self.start >= self.end:
            raise ValueError("provider request start must be earlier than end")
        return self


class ProviderDownloadResult(FXLabBaseModel):
    """Output of a provider download call."""

    provider_name: str
    raw_artifact_paths: tuple[Path, ...]
    request: ProviderRequest
    retrieved_at: datetime
    provider_payload_format: str
    source_instrument: str
    provider_timeframe: str

    @field_validator("retrieved_at")
    @classmethod
    def validate_retrieved_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("retrieved_at must be timezone-aware")
        return value.astimezone(UTC)


class HistoricalDataProvider(ABC):
    """Internal provider abstraction used by the rest of the lab."""

    provider_name: str

    @abstractmethod
    def download(self, request: ProviderRequest) -> ProviderDownloadResult:
        """Download historical data through the internal provider contract."""


class HistoricalDataProviderError(Exception):
    """Base exception for provider failures."""


class UnsupportedInstrumentError(HistoricalDataProviderError):
    """Raised when an internal pair cannot be mapped to the provider."""


class UnsupportedTimeframeError(HistoricalDataProviderError):
    """Raised when an internal timeframe cannot be mapped to the provider."""
