"""Feature engine contracts."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from fxlab.domain.bars import CanonicalBar


@dataclass(frozen=True)
class FeatureSpec:
    """Declarative feature specification."""

    name: str
    params: dict[str, Any]
    warmup_bars: int = 0
    requires_shift: bool = True


@dataclass(frozen=True)
class FeatureComputationResult:
    """Computed feature output keyed to canonical bars."""

    spec: FeatureSpec
    columns: tuple[str, ...]
    rows: tuple[dict[str, object], ...]


class Feature(ABC):
    """Abstract feature contract."""

    spec: FeatureSpec

    @abstractmethod
    def compute(self, bars: tuple[CanonicalBar, ...]) -> FeatureComputationResult:
        """Compute feature values from canonical bars."""
