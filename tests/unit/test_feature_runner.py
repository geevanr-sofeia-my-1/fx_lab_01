"""Feature runner tests."""

from dataclasses import dataclass
from datetime import UTC, datetime

from fxlab.domain.bars import CanonicalBar
from fxlab.features.base import Feature, FeatureComputationResult, FeatureSpec
from fxlab.features.registry import FeatureRegistry
from fxlab.features.runner import run_feature_job


@dataclass
class CloseEchoFeature(Feature):
    spec: FeatureSpec

    def compute(self, bars: tuple[CanonicalBar, ...]) -> FeatureComputationResult:
        return FeatureComputationResult(
            spec=self.spec,
            columns=("close_echo",),
            rows=tuple(
                {
                    "timestamp": bar.timestamp.isoformat(),
                    "close_echo": bar.close,
                }
                for bar in bars
            ),
        )


def test_run_feature_job_is_deterministic() -> None:
    bars = (
        CanonicalBar(
            pair="EURUSD",
            timeframe="1H",
            timestamp=datetime(2024, 1, 1, tzinfo=UTC),
            open=1.1,
            high=1.2,
            low=1.0,
            close=1.15,
            source="fixture",
            price_basis="mid",
        ),
    )
    registry = FeatureRegistry()
    registry.register(
        "close_echo",
        lambda **params: CloseEchoFeature(FeatureSpec("close_echo", dict(params))),
    )

    left = run_feature_job(registry, "close_echo", bars, tag="a")
    right = run_feature_job(registry, "close_echo", bars, tag="a")

    assert left.fingerprint == right.fingerprint
    assert left.feature_name == "close_echo_tag_a"
