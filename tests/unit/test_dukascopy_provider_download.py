"""Mocked Dukascopy download flow tests."""

import shutil
import uuid
from datetime import UTC, datetime
from pathlib import Path

from fxlab.data.providers.base import ProviderRequest
from fxlab.data.providers.dukascopy import DukascopyProvider, plan_chunks


def test_plan_chunks_splits_request_deterministically() -> None:
    request = ProviderRequest(
        pair="EURUSD",
        timeframe="1H",
        start=datetime(2024, 1, 1, tzinfo=UTC),
        end=datetime(2024, 1, 4, tzinfo=UTC),
        price_basis="mid",
        chunk_size_days=1,
    )

    chunks = plan_chunks(request)

    assert len(chunks) == 3
    assert chunks[0] == (datetime(2024, 1, 1, tzinfo=UTC), datetime(2024, 1, 2, tzinfo=UTC))
    assert chunks[-1] == (datetime(2024, 1, 3, tzinfo=UTC), datetime(2024, 1, 4, tzinfo=UTC))


def test_mocked_download_writes_chunked_artifacts() -> None:
    scratch = Path("artifacts") / "cache" / f"test_dukascopy_download_{uuid.uuid4().hex}"
    scratch.mkdir(parents=True, exist_ok=True)
    calls: list[tuple[str, str, datetime, datetime, str]] = []

    def fake_fetcher(
        source_instrument: str,
        provider_timeframe: str,
        start: datetime,
        end: datetime,
        price_basis: str,
    ) -> bytes:
        calls.append((source_instrument, provider_timeframe, start, end, price_basis))
        payload = (
            f"{source_instrument}|{provider_timeframe}|"
            f"{start.isoformat()}|{end.isoformat()}"
        )
        return payload.encode()

    try:
        provider = DukascopyProvider(fetcher=fake_fetcher, repo_root=scratch)
        request = ProviderRequest(
            pair="EURUSD",
            timeframe="1H",
            start=datetime(2024, 1, 1, tzinfo=UTC),
            end=datetime(2024, 1, 3, tzinfo=UTC),
            price_basis="mid",
            chunk_size_days=1,
        )

        result = provider.download(request)

        assert len(calls) == 2
        assert len(result.raw_artifact_paths) == 2
        assert result.raw_artifact_paths[0].name == "chunk_0001.bin"
        assert result.raw_artifact_paths[0].read_bytes().startswith(b"EURUSD|1h|")
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
