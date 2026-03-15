"""Dukascopy provider adapter."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from pathlib import Path

from fxlab.data.download.storage import raw_download_directory
from fxlab.data.providers.base import (
    HistoricalDataProvider,
    ProviderDownloadResult,
    ProviderRequest,
)
from fxlab.data.providers.mapping import map_pair_to_dukascopy, map_timeframe_to_dukascopy

Fetcher = Callable[[str, str, datetime, datetime, str], bytes]


def _default_fetcher(
    source_instrument: str,
    provider_timeframe: str,
    start: datetime,
    end: datetime,
    price_basis: str,
) -> bytes:
    raise NotImplementedError(
        "Real Dukascopy network download is not wired yet. "
        "Inject a fetcher for tests or the next slice."
    )


def plan_chunks(request: ProviderRequest) -> tuple[tuple[datetime, datetime], ...]:
    """Split a request into deterministic chunks."""
    if request.chunk_size_days is None:
        return ((request.start, request.end),)

    chunks: list[tuple[datetime, datetime]] = []
    chunk_start = request.start
    chunk_delta = timedelta(days=request.chunk_size_days)
    while chunk_start < request.end:
        chunk_end = min(chunk_start + chunk_delta, request.end)
        chunks.append((chunk_start, chunk_end))
        chunk_start = chunk_end
    return tuple(chunks)


class DukascopyProvider(HistoricalDataProvider):
    """Internal Dukascopy provider adapter."""

    provider_name = "dukascopy"

    def __init__(
        self,
        *,
        fetcher: Fetcher | None = None,
        repo_root: Path | None = None,
    ) -> None:
        self._fetcher = fetcher or _default_fetcher
        self._repo_root = repo_root

    def download(self, request: ProviderRequest) -> ProviderDownloadResult:
        """Download raw provider payloads into deterministic artifact paths."""
        source_instrument = map_pair_to_dukascopy(request.pair)
        provider_timeframe = map_timeframe_to_dukascopy(request.timeframe)
        chunk_windows = plan_chunks(request)
        download_job_id = f"{request.start:%Y%m%dT%H%M%SZ}_{request.end:%Y%m%dT%H%M%SZ}"
        target_dir = raw_download_directory(
            request.pair,
            request.timeframe,
            download_job_id,
            repo_root=self._repo_root,
        )
        target_dir.mkdir(parents=True, exist_ok=True)

        artifact_paths: list[Path] = []
        for index, (chunk_start, chunk_end) in enumerate(chunk_windows, start=1):
            payload = self._fetcher(
                source_instrument,
                provider_timeframe,
                chunk_start,
                chunk_end,
                request.price_basis,
            )
            artifact_path = target_dir / f"chunk_{index:04d}.bin"
            artifact_path.write_bytes(payload)
            artifact_paths.append(artifact_path)

        return ProviderDownloadResult(
            provider_name=self.provider_name,
            raw_artifact_paths=tuple(artifact_paths),
            request=request,
            retrieved_at=datetime.now(tz=UTC),
            provider_payload_format="binary",
            source_instrument=source_instrument,
            provider_timeframe=provider_timeframe,
        )
