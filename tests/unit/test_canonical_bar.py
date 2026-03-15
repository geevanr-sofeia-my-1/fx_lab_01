"""Canonical bar schema tests."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from fxlab.domain.bars import CanonicalBar


def test_canonical_bar_validates_happy_path() -> None:
    bar = CanonicalBar(
        pair="EURUSD",
        timeframe="1H",
        timestamp=datetime(2024, 1, 1, 0, 0, tzinfo=UTC),
        open=1.1,
        high=1.2,
        low=1.0,
        close=1.15,
        source="fixture",
        price_basis="mid",
    )

    assert bar.provider == "dukascopy"
    assert bar.timestamp.tzinfo == UTC


def test_canonical_bar_rejects_naive_timestamps() -> None:
    with pytest.raises(ValidationError):
        CanonicalBar(
            pair="EURUSD",
            timeframe="1H",
            timestamp=datetime(2024, 1, 1, 0, 0),
            open=1.1,
            high=1.2,
            low=1.0,
            close=1.15,
            source="fixture",
            price_basis="mid",
        )


def test_canonical_bar_rejects_invalid_ohlc() -> None:
    with pytest.raises(ValidationError):
        CanonicalBar(
            pair="EURUSD",
            timeframe="1H",
            timestamp=datetime(2024, 1, 1, 0, 0, tzinfo=UTC),
            open=1.1,
            high=1.05,
            low=1.0,
            close=1.15,
            source="fixture",
            price_basis="mid",
        )
