"""Momentum feature implementations."""

from __future__ import annotations

from dataclasses import dataclass

from fxlab.domain.bars import CanonicalBar
from fxlab.features.alignment import shift_values
from fxlab.features.base import Feature, FeatureComputationResult, FeatureSpec
from fxlab.features.naming import feature_instance_name


@dataclass
class RSIFeature(Feature):
    """Wilder-style RSI feature."""

    spec: FeatureSpec

    def compute(self, bars: tuple[CanonicalBar, ...]) -> FeatureComputationResult:
        length = int(self.spec.params["length"])
        closes = tuple(bar.close for bar in bars)
        values: list[float | None] = []
        gains: list[float] = []
        losses: list[float] = []
        avg_gain: float | None = None
        avg_loss: float | None = None

        for index in range(len(closes)):
            if index == 0:
                values.append(None)
                continue

            change = closes[index] - closes[index - 1]
            gains.append(max(change, 0.0))
            losses.append(max(-change, 0.0))

            if index < length:
                values.append(None)
                continue

            if avg_gain is None or avg_loss is None:
                avg_gain = sum(gains[:length]) / length
                avg_loss = sum(losses[:length]) / length
            else:
                avg_gain = ((avg_gain * (length - 1)) + gains[-1]) / length
                avg_loss = ((avg_loss * (length - 1)) + losses[-1]) / length

            if avg_loss == 0:
                rsi = 100.0
            else:
                rs = avg_gain / avg_loss
                rsi = 100.0 - (100.0 / (1.0 + rs))
            values.append(rsi)

        shifted = (
            shift_values(tuple(values), periods=1)
            if self.spec.requires_shift
            else tuple(values)
        )
        column_name = feature_instance_name(self.spec)
        return FeatureComputationResult(
            spec=self.spec,
            columns=(column_name,),
            rows=tuple(
                {
                    "timestamp": bar.timestamp.isoformat(),
                    column_name: shifted[index],
                }
                for index, bar in enumerate(bars)
            ),
        )


def make_rsi_feature(*, length: int, requires_shift: bool = True) -> RSIFeature:
    """Factory for RSI."""
    return RSIFeature(
        FeatureSpec(
            name="rsi",
            params={"length": length},
            warmup_bars=length,
            requires_shift=requires_shift,
        )
    )
