"""Provider contract tests."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from fxlab.data.providers.base import ProviderDownloadResult, ProviderRequest
from fxlab.data.providers.dukascopy import DukascopyProvider


def test_provider_request_requires_valid_time_window() -> None:
    with pytest.raises(ValidationError):
        ProviderRequest(
            pair="EURUSD",
            timeframe="1H",
            start=datetime(2024, 2, 1, tzinfo=UTC),
            end=datetime(2024, 1, 1, tzinfo=UTC),
            price_basis="mid",
        )


def test_provider_download_result_requires_timezone_aware_timestamp() -> None:
    request = ProviderRequest(
        pair="EURUSD",
        timeframe="1H",
        start=datetime(2024, 1, 1, tzinfo=UTC),
        end=datetime(2024, 2, 1, tzinfo=UTC),
        price_basis="mid",
    )
    with pytest.raises(ValidationError):
        ProviderDownloadResult(
            provider_name="dukascopy",
            raw_artifact_paths=(),
            request=request,
            retrieved_at=datetime(2024, 1, 2),
            provider_payload_format="csv",
            source_instrument="EURUSD",
            provider_timeframe="1h",
        )


def test_dukascopy_provider_resolves_mapped_request() -> None:
    provider = DukascopyProvider(fetcher=lambda *_args: b"fixture")
    request = ProviderRequest(
        pair="EURUSD",
        timeframe="1H",
        start=datetime(2024, 1, 1, tzinfo=UTC),
        end=datetime(2024, 2, 1, tzinfo=UTC),
        price_basis="mid",
    )

    result = provider.download(request)

    assert result.provider_name == "dukascopy"
    assert result.source_instrument == "EURUSD"
    assert result.provider_timeframe == "1h"
