"""SMA feature tests."""

from datetime import UTC, datetime, timedelta

from fxlab.domain.bars import CanonicalBar
from fxlab.features.trend import make_sma_feature


def _bars() -> tuple[CanonicalBar, ...]:
    return tuple(
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


def test_sma_feature_respects_warmup_and_shift() -> None:
    feature = make_sma_feature(length=3)
    result = feature.compute(_bars())
    values = [row["sma_length_3"] for row in result.rows]

    assert values == [None, None, None, 2.0]


def test_sma_feature_can_disable_shift() -> None:
    feature = make_sma_feature(length=3, requires_shift=False)
    result = feature.compute(_bars())
    values = [row["sma_length_3"] for row in result.rows]

    assert values == [None, None, 2.0, 3.0]
