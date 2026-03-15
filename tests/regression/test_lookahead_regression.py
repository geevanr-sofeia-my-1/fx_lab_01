"""Regression tests for feature lookahead protection."""

from datetime import UTC, datetime, timedelta

from fxlab.domain.bars import CanonicalBar
from fxlab.features.trend import make_sma_feature


def test_shifted_sma_does_not_use_current_bar_information() -> None:
    bars = tuple(
        CanonicalBar(
            pair="EURUSD",
            timeframe="1H",
            timestamp=datetime(2024, 1, 1, tzinfo=UTC) + timedelta(hours=index),
            open=1.0 + index,
            high=1.2 + index,
            low=0.9 + index,
            close=1.0 + index,
            source="fixture",
            price_basis="mid",
        )
        for index in range(4)
    )

    shifted = make_sma_feature(length=3, requires_shift=True).compute(bars)
    unshifted = make_sma_feature(length=3, requires_shift=False).compute(bars)

    assert shifted.rows[2]["sma_length_3"] is None
    assert unshifted.rows[2]["sma_length_3"] == 2.0
