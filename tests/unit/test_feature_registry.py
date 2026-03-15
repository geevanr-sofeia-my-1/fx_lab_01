"""Feature registry tests."""

from dataclasses import dataclass

import pytest

from fxlab.features.base import Feature, FeatureComputationResult, FeatureSpec
from fxlab.features.registry import FeatureRegistry


@dataclass
class DummyFeature(Feature):
    spec: FeatureSpec

    def compute(self, bars: tuple[object, ...]) -> FeatureComputationResult:
        return FeatureComputationResult(spec=self.spec, columns=("dummy",), rows=())


def test_feature_registry_registers_and_creates_features() -> None:
    registry = FeatureRegistry()
    registry.register("dummy", lambda **params: DummyFeature(FeatureSpec("dummy", params)))

    feature = registry.create("dummy", length=5)

    assert feature.spec.params["length"] == 5
    assert registry.names() == ("dummy",)


def test_feature_registry_rejects_duplicates() -> None:
    registry = FeatureRegistry()
    registry.register("dummy", lambda **params: DummyFeature(FeatureSpec("dummy", params)))
    with pytest.raises(ValueError):
        registry.register("dummy", lambda **params: DummyFeature(FeatureSpec("dummy", params)))
