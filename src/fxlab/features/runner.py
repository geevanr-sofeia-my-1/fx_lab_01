"""Minimal feature job runner."""

from __future__ import annotations

from dataclasses import dataclass

from fxlab.domain.bars import CanonicalBar
from fxlab.features.base import FeatureComputationResult
from fxlab.features.naming import feature_instance_name
from fxlab.features.registry import FeatureRegistry
from fxlab.utils.hashing import sha256_bytes


@dataclass(frozen=True)
class FeatureJobResult:
    """Feature job output metadata."""

    feature_name: str
    fingerprint: str
    rows: tuple[dict[str, object], ...]


def run_feature_job(
    registry: FeatureRegistry,
    feature_name: str,
    bars: tuple[CanonicalBar, ...],
    **params: object,
) -> FeatureJobResult:
    """Run one feature computation deterministically."""
    feature = registry.create(feature_name, **params)
    result: FeatureComputationResult = feature.compute(bars)
    instance_name = feature_instance_name(result.spec)
    serialized = repr((instance_name, result.columns, result.rows)).encode("utf-8")
    fingerprint = sha256_bytes(serialized)
    return FeatureJobResult(
        feature_name=instance_name,
        fingerprint=fingerprint,
        rows=result.rows,
    )
