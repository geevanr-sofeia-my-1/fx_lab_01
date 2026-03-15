"""EMA feature tests."""

from datetime import UTC, datetime, timedelta

from fxlab.domain.bars import CanonicalBar
from fxlab.features.trend import make_ema_feature


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
        for index in range(5)
    )


def test_ema_feature_respects_seed_and_shift() -> None:
    feature = make_ema_feature(length=3)
    result = feature.compute(_bars())
    values = [row["ema_length_3"] for row in result.rows]

    assert values[0] is None
    assert values[1] is None
    assert values[2] is None
    assert values[3] == 2.0
    assert values[4] == 3.0
