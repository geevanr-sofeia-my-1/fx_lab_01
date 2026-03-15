"""Canonical normalization tests."""

from datetime import UTC, datetime, timedelta

import pytest

from fxlab.data.normalize.canonical import normalize_raw_bars


def test_normalize_raw_bars_sorts_rows_and_keeps_unique_timestamps() -> None:
    rows = [
        {
            "timestamp": datetime(2024, 1, 1, 1, tzinfo=UTC),
            "open": 1.2,
            "high": 1.3,
            "low": 1.1,
            "close": 1.25,
        },
        {
            "timestamp": datetime(2024, 1, 1, 0, tzinfo=UTC),
            "open": 1.1,
            "high": 1.2,
            "low": 1.0,
            "close": 1.15,
        },
    ]

    bars = normalize_raw_bars(
        rows,
        pair="EURUSD",
        timeframe="1H",
        source="fixture",
        provider="dukascopy",
        price_basis="mid",
    )

    assert [bar.timestamp for bar in bars] == [
        datetime(2024, 1, 1, 0, tzinfo=UTC),
        datetime(2024, 1, 1, 1, tzinfo=UTC),
    ]


def test_normalize_raw_bars_drops_duplicate_timestamps_by_default() -> None:
    row = {
        "timestamp": datetime(2024, 1, 1, 0, tzinfo=UTC),
        "open": 1.1,
        "high": 1.2,
        "low": 1.0,
        "close": 1.15,
    }

    bars = normalize_raw_bars(
        [row, row],
        pair="EURUSD",
        timeframe="1H",
        source="fixture",
        provider="dukascopy",
        price_basis="mid",
    )

    assert len(bars) == 1


def test_normalize_raw_bars_can_reject_duplicate_timestamps() -> None:
    row = {
        "timestamp": datetime(2024, 1, 1, 0, tzinfo=UTC),
        "open": 1.1,
        "high": 1.2,
        "low": 1.0,
        "close": 1.15,
    }

    with pytest.raises(ValueError):
        normalize_raw_bars(
            [row, row],
            pair="EURUSD",
            timeframe="1H",
            source="fixture",
            provider="dukascopy",
            price_basis="mid",
            drop_duplicates=False,
        )


def test_normalize_raw_bars_preserves_optional_fields() -> None:
    rows = [
        {
            "timestamp": datetime(2024, 1, 1, 0, tzinfo=UTC) + timedelta(hours=offset),
            "open": 1.1 + offset * 0.01,
            "high": 1.2 + offset * 0.01,
            "low": 1.0 + offset * 0.01,
            "close": 1.15 + offset * 0.01,
            "volume": 100 + offset,
            "tick_volume": 200 + offset,
            "spread": 0.0001,
            "session_london": offset == 1,
        }
        for offset in range(2)
    ]

    bars = normalize_raw_bars(
        rows,
        pair="EURUSD",
        timeframe="1H",
        source="fixture",
        provider="dukascopy",
        price_basis="mid",
        source_instrument="EURUSD",
    )

    assert bars[0].volume == 100.0
    assert bars[1].session_london is True
    assert bars[0].source_instrument == "EURUSD"


def test_normalize_raw_bars_derives_sessions_and_preserves_price_basis() -> None:
    rows = [
        {
            "timestamp": datetime(2024, 1, 1, 13, tzinfo=UTC),
            "open": 1.1,
            "high": 1.2,
            "low": 1.0,
            "close": 1.15,
        }
    ]

    bars = normalize_raw_bars(
        rows,
        pair="EURUSD",
        timeframe="1H",
        source="fixture",
        provider="dukascopy",
        price_basis="mid",
    )

    assert bars[0].price_basis == "mid"
    assert bars[0].session_london is True
    assert bars[0].session_newyork is True
