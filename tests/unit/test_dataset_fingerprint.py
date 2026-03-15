"""Dataset fingerprint tests."""

from datetime import UTC, datetime, timedelta

from fxlab.data.normalize.canonical import normalize_raw_bars
from fxlab.data.normalize.quality import build_dataset_fingerprint


def _rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp": datetime(2024, 1, 1, 0, tzinfo=UTC) + timedelta(hours=offset),
            "open": 1.1 + offset * 0.01,
            "high": 1.2 + offset * 0.01,
            "low": 1.0 + offset * 0.01,
            "close": 1.15 + offset * 0.01,
        }
        for offset in range(3)
    ]


def test_dataset_fingerprint_is_deterministic() -> None:
    bars = normalize_raw_bars(
        _rows(),
        pair="EURUSD",
        timeframe="1H",
        source="fixture",
        provider="dukascopy",
        price_basis="mid",
    )

    left = build_dataset_fingerprint(bars, preprocessing_version="1")
    right = build_dataset_fingerprint(bars, preprocessing_version="1")

    assert left.fingerprint == right.fingerprint
    assert left.row_count == 3


def test_dataset_fingerprint_changes_when_data_changes() -> None:
    bars = normalize_raw_bars(
        _rows(),
        pair="EURUSD",
        timeframe="1H",
        source="fixture",
        provider="dukascopy",
        price_basis="mid",
    )
    changed_rows = _rows()
    changed_rows[1]["open"] = 1.5
    changed_rows[1]["high"] = 1.6
    changed_rows[1]["low"] = 1.4
    changed_rows[1]["close"] = 1.55
    changed_bars = normalize_raw_bars(
        changed_rows,
        pair="EURUSD",
        timeframe="1H",
        source="fixture",
        provider="dukascopy",
        price_basis="mid",
    )

    original = build_dataset_fingerprint(bars, preprocessing_version="1")
    changed = build_dataset_fingerprint(changed_bars, preprocessing_version="1")

    assert original.fingerprint != changed.fingerprint
