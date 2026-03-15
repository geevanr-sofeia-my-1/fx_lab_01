"""ATR feature tests."""

from datetime import UTC, datetime, timedelta

from fxlab.domain.bars import CanonicalBar
from fxlab.features.volatility import make_atr_feature


def _bars() -> tuple[CanonicalBar, ...]:
    payload = (
        (1.0, 1.2, 0.9, 1.1),
        (1.1, 1.3, 1.0, 1.2),
        (1.2, 1.4, 1.1, 1.3),
        (1.3, 1.5, 1.2, 1.4),
    )
    return tuple(
        CanonicalBar(
            pair="EURUSD",
            timeframe="1H",
            timestamp=datetime(2024, 1, 1, tzinfo=UTC) + timedelta(hours=index),
            open=open_,
            high=high,
            low=low,
            close=close,
            source="fixture",
            price_basis="mid",
        )
        for index, (open_, high, low, close) in enumerate(payload)
    )


def test_atr_feature_respects_warmup_and_shift() -> None:
    feature = make_atr_feature(length=3)
    result = feature.compute(_bars())
    values = [row["atr_length_3"] for row in result.rows]

    assert values[:3] == [None, None, None]
    assert values[3] is not None
