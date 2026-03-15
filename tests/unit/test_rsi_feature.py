"""RSI feature tests."""

from datetime import UTC, datetime, timedelta

from fxlab.domain.bars import CanonicalBar
from fxlab.features.momentum import make_rsi_feature


def _bars() -> tuple[CanonicalBar, ...]:
    closes = (1.0, 2.0, 3.0, 2.0, 3.0, 4.0)
    return tuple(
        CanonicalBar(
            pair="EURUSD",
            timeframe="1H",
            timestamp=datetime(2024, 1, 1, tzinfo=UTC) + timedelta(hours=index),
            open=close,
            high=close + 0.2,
            low=close - 0.2,
            close=close,
            source="fixture",
            price_basis="mid",
        )
        for index, close in enumerate(closes)
    )


def test_rsi_feature_outputs_shifted_values_after_warmup() -> None:
    feature = make_rsi_feature(length=3)
    result = feature.compute(_bars())
    values = [row["rsi_length_3"] for row in result.rows]

    assert values[:4] == [None, None, None, None]
    assert values[4] is not None
    assert values[5] is not None
