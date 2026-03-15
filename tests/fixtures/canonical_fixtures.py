"""Small deterministic canonical raw-row fixtures."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta


def clean_hourly_rows() -> list[dict[str, object]]:
    """Return a simple clean hourly OHLC fixture."""
    return [
        {
            "timestamp": datetime(2024, 1, 1, 0, tzinfo=UTC) + timedelta(hours=offset),
            "open": 1.10 + offset * 0.01,
            "high": 1.20 + offset * 0.01,
            "low": 1.00 + offset * 0.01,
            "close": 1.15 + offset * 0.01,
            "volume": 100 + offset,
        }
        for offset in range(4)
    ]


def duplicate_timestamp_rows() -> list[dict[str, object]]:
    """Return rows with a deliberate duplicate timestamp."""
    base = clean_hourly_rows()
    return [base[0], base[0], *base[1:]]


def same_bar_ambiguity_rows() -> list[dict[str, object]]:
    """Return bars suitable for later stop/target ambiguity tests."""
    return [
        {
            "timestamp": datetime(2024, 1, 1, 0, tzinfo=UTC),
            "open": 1.1000,
            "high": 1.1010,
            "low": 1.0990,
            "close": 1.1005,
        },
        {
            "timestamp": datetime(2024, 1, 1, 1, tzinfo=UTC),
            "open": 1.1005,
            "high": 1.1050,
            "low": 1.0950,
            "close": 1.1000,
        },
    ]


def session_boundary_rows() -> list[dict[str, object]]:
    """Return rows around session transitions."""
    timestamps = (
        datetime(2024, 1, 1, 7, tzinfo=UTC),
        datetime(2024, 1, 1, 8, tzinfo=UTC),
        datetime(2024, 1, 1, 13, tzinfo=UTC),
    )
    return [
        {
            "timestamp": ts,
            "open": 1.1,
            "high": 1.2,
            "low": 1.0,
            "close": 1.15,
        }
        for ts in timestamps
    ]
