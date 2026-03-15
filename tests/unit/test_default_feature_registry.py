"""Default feature registry tests."""

from fxlab.features.defaults import build_default_feature_registry


def test_default_feature_registry_contains_core_features() -> None:
    registry = build_default_feature_registry()
    assert registry.names() == ("atr", "ema", "rsi", "sma")
