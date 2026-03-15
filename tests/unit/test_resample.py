"""Resampling tests."""

from datetime import UTC, datetime, timedelta

import pytest

from fxlab.data.normalize.canonical import normalize_raw_bars
from fxlab.data.normalize.resample import resample_bars


def _hourly_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp": datetime(2024, 1, 1, 0, tzinfo=UTC) + timedelta(hours=offset),
            "open": 1.0 + offset * 0.1,
            "high": 1.05 + offset * 0.1,
            "low": 0.95 + offset * 0.1,
            "close": 1.02 + offset * 0.1,
            "volume": 10 + offset,
        }
        for offset in range(4)
    ]


def test_resample_bars_aggregates_ohlc_deterministically() -> None:
    bars = normalize_raw_bars(
        _hourly_rows(),
        pair="EURUSD",
        timeframe="1H",
        source="fixture",
        provider="dukascopy",
        price_basis="mid",
    )

    result = resample_bars(bars, target_timeframe="4H")

    assert len(result) == 1
    assert result[0].open == 1.0
    assert result[0].high == 1.35
    assert result[0].low == 0.95
    assert result[0].close == 1.32
    assert result[0].volume == 46.0


def test_resample_bars_rejects_non_higher_timeframe() -> None:
    bars = normalize_raw_bars(
        _hourly_rows(),
        pair="EURUSD",
        timeframe="1H",
        source="fixture",
        provider="dukascopy",
        price_basis="mid",
    )

    with pytest.raises(ValueError):
        resample_bars(bars, target_timeframe="1H")
