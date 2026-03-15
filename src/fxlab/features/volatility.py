"""Volatility feature implementations."""

from __future__ import annotations

from dataclasses import dataclass

from fxlab.domain.bars import CanonicalBar
from fxlab.features.alignment import shift_values
from fxlab.features.base import Feature, FeatureComputationResult, FeatureSpec
from fxlab.features.naming import feature_instance_name


@dataclass
class ATRFeature(Feature):
    """Wilder-style ATR feature."""

    spec: FeatureSpec

    def compute(self, bars: tuple[CanonicalBar, ...]) -> FeatureComputationResult:
        length = int(self.spec.params["length"])
        true_ranges: list[float] = []
        values: list[float | None] = []
        atr: float | None = None

        for index, bar in enumerate(bars):
            if index == 0:
                tr = bar.high - bar.low
            else:
                prev_close = bars[index - 1].close
                tr = max(
                    bar.high - bar.low,
                    abs(bar.high - prev_close),
                    abs(bar.low - prev_close),
                )
            true_ranges.append(tr)

            if index + 1 < length:
                values.append(None)
                continue

            if atr is None:
                atr = sum(true_ranges[:length]) / length
            else:
                atr = ((atr * (length - 1)) + true_ranges[-1]) / length
            values.append(atr)

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


def make_atr_feature(*, length: int, requires_shift: bool = True) -> ATRFeature:
    """Factory for ATR."""
    return ATRFeature(
        FeatureSpec(
            name="atr",
            params={"length": length},
            warmup_bars=length - 1,
            requires_shift=requires_shift,
        )
    )
