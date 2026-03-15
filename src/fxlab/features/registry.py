"""Feature registration and lookup."""

from __future__ import annotations

from collections.abc import Callable

from fxlab.features.base import Feature

FeatureFactory = Callable[..., Feature]


class FeatureRegistry:
    """In-memory registry of feature factories."""

    def __init__(self) -> None:
        self._factories: dict[str, FeatureFactory] = {}

    def register(self, name: str, factory: FeatureFactory) -> None:
        """Register a feature factory by stable name."""
        if name in self._factories:
            raise ValueError(f"feature already registered: {name}")
        self._factories[name] = factory

    def create(self, name: str, **params: object) -> Feature:
        """Instantiate a registered feature."""
        try:
            factory = self._factories[name]
        except KeyError as exc:
            raise KeyError(f"unknown feature: {name}") from exc
        return factory(**params)

    def names(self) -> tuple[str, ...]:
        """Return registered feature names in sorted order."""
        return tuple(sorted(self._factories))
