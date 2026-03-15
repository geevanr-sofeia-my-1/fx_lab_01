"""Raw download manifest models and writers."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from pydantic import field_validator

from fxlab.config.schema_base import FXLabBaseModel
from fxlab.data.providers.base import ProviderDownloadResult, ProviderRequest
from fxlab.domain.enums import PriceBasis
from fxlab.utils.hashing import sha256_file


class RawArtifactManifestEntry(FXLabBaseModel):
    """Metadata about a single raw provider artifact."""

    path: Path
    sha256: str


class RawDownloadManifest(FXLabBaseModel):
    """Manifest persisted for every raw download job."""

    schema_version: str = "1"
    provider_name: str
    package_version: str
    pair: str
    timeframe: str
    request_start: datetime
    request_end: datetime
    retrieved_at: datetime
    source_instrument: str
    provider_timeframe: str
    price_basis: PriceBasis
    artifacts: tuple[RawArtifactManifestEntry, ...]
    preprocessing_version: str

    @field_validator("request_start", "request_end", "retrieved_at")
    @classmethod
    def validate_timestamps(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("manifest timestamps must be timezone-aware")
        return value.astimezone(UTC)


def build_raw_download_manifest(
    result: ProviderDownloadResult,
    *,
    package_version: str,
    preprocessing_version: str,
) -> RawDownloadManifest:
    """Create a manifest from a provider download result."""
    entries = tuple(
        RawArtifactManifestEntry(path=artifact, sha256=sha256_file(artifact))
        for artifact in result.raw_artifact_paths
    )
    request: ProviderRequest = result.request
    return RawDownloadManifest(
        provider_name=result.provider_name,
        package_version=package_version,
        pair=request.pair,
        timeframe=request.timeframe,
        request_start=request.start,
        request_end=request.end,
        retrieved_at=result.retrieved_at,
        source_instrument=result.source_instrument,
        provider_timeframe=result.provider_timeframe,
        price_basis=request.price_basis,
        artifacts=entries,
        preprocessing_version=preprocessing_version,
    )


def write_raw_download_manifest(manifest: RawDownloadManifest, destination: Path) -> None:
    """Write a raw download manifest as deterministic JSON."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(manifest.model_dump(mode="json"), indent=2, sort_keys=True),
        encoding="utf-8",
    )
