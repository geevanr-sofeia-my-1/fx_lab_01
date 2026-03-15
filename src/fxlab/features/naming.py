"""Stable feature naming helpers."""

from __future__ import annotations

from fxlab.features.base import FeatureSpec


def feature_instance_name(spec: FeatureSpec) -> str:
    """Build a stable machine-readable feature instance name."""
    if not spec.params:
        return spec.name
    ordered = "_".join(f"{key}_{spec.params[key]}" for key in sorted(spec.params))
    return f"{spec.name}_{ordered}"
