"""Default feature registry bootstrap."""

from __future__ import annotations

from fxlab.features.momentum import make_rsi_feature
from fxlab.features.registry import FeatureRegistry
from fxlab.features.trend import make_ema_feature, make_sma_feature
from fxlab.features.volatility import make_atr_feature


def build_default_feature_registry() -> FeatureRegistry:
    """Build the default in-process feature registry."""
    registry = FeatureRegistry()
    registry.register("sma", lambda **params: make_sma_feature(**params))
    registry.register("ema", lambda **params: make_ema_feature(**params))
    registry.register("rsi", lambda **params: make_rsi_feature(**params))
    registry.register("atr", lambda **params: make_atr_feature(**params))
    return registry
