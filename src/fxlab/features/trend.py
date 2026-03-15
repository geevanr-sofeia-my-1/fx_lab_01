"""Trend feature implementations."""

from __future__ import annotations

from dataclasses import dataclass

from fxlab.domain.bars import CanonicalBar
from fxlab.features.alignment import rolling_mean, shift_values
from fxlab.features.base import Feature, FeatureComputationResult, FeatureSpec
from fxlab.features.naming import feature_instance_name


@dataclass
class SMAFeature(Feature):
    """Simple moving average feature."""

    spec: FeatureSpec

    def compute(self, bars: tuple[CanonicalBar, ...]) -> FeatureComputationResult:
        length = int(self.spec.params["length"])
        closes = tuple(bar.close for bar in bars)
        values = rolling_mean(closes, window=length)
        if self.spec.requires_shift:
            values = shift_values(values, periods=1)
        column_name = feature_instance_name(self.spec)
        return FeatureComputationResult(
            spec=self.spec,
            columns=(column_name,),
            rows=tuple(
                {
                    "timestamp": bar.timestamp.isoformat(),
                    column_name: values[index],
                }
                for index, bar in enumerate(bars)
            ),
        )


def make_sma_feature(*, length: int, requires_shift: bool = True) -> SMAFeature:
    """Factory for a simple moving average feature."""
    return SMAFeature(
        FeatureSpec(
            name="sma",
            params={"length": length},
            warmup_bars=length - 1,
            requires_shift=requires_shift,
        )
    )


@dataclass
class EMAFeature(Feature):
    """Exponential moving average feature."""

    spec: FeatureSpec

    def compute(self, bars: tuple[CanonicalBar, ...]) -> FeatureComputationResult:
        length = int(self.spec.params["length"])
        closes = tuple(bar.close for bar in bars)
        alpha = 2.0 / (length + 1.0)
        values: list[float | None] = []
        ema: float | None = None
        for index, close in enumerate(closes):
            if index + 1 < length:
                values.append(None)
                continue
            if ema is None:
                seed = sum(closes[index + 1 - length : index + 1]) / length
                ema = seed
            else:
                ema = (close - ema) * alpha + ema
            values.append(ema)
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


def make_ema_feature(*, length: int, requires_shift: bool = True) -> EMAFeature:
    """Factory for an exponential moving average feature."""
    return EMAFeature(
        FeatureSpec(
            name="ema",
            params={"length": length},
            warmup_bars=length - 1,
            requires_shift=requires_shift,
        )
    )
