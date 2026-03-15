"""Dataset quality summary tests."""

from datetime import UTC, datetime, timedelta

from fxlab.data.normalize.canonical import normalize_raw_bars
from fxlab.data.normalize.quality import summarize_dataset_quality


def test_summarize_dataset_quality_reports_expected_counts() -> None:
    rows = [
        {
            "timestamp": datetime(2024, 1, 1, 0, tzinfo=UTC) + timedelta(hours=offset),
            "open": 1.1 + offset * 0.01,
            "high": 1.2 + offset * 0.01,
            "low": 1.0 + offset * 0.01,
            "close": 1.15 + offset * 0.01,
            "volume": None if offset == 0 else 100,
            "tick_volume": None if offset == 1 else 200,
            "spread": None if offset == 2 else 0.0001,
        }
        for offset in range(3)
    ]
    bars = normalize_raw_bars(
        rows,
        pair="EURUSD",
        timeframe="1H",
        source="fixture",
        provider="dukascopy",
        price_basis="mid",
    )

    summary = summarize_dataset_quality(bars)

    assert summary.row_count == 3
    assert summary.duplicate_count == 0
    assert summary.null_volume_count == 1
    assert summary.null_tick_volume_count == 1
    assert summary.null_spread_count == 1
