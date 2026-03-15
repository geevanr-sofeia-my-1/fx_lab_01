"""Deterministic UTC session labeling."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SessionLabels:
    """Session membership flags for a UTC timestamp."""

    asia: bool
    london: bool
    newyork: bool


def label_sessions(timestamp: datetime) -> SessionLabels:
    """Assign Asia, London, and New York session flags in UTC.

    Initial conservative definitions:
    - Asia: 00:00-07:59 UTC
    - London: 08:00-15:59 UTC
    - New York: 13:00-20:59 UTC

    Overlaps are intentional and preserved.
    """
    if timestamp.tzinfo is None:
        raise ValueError("session labeling requires timezone-aware timestamps")

    hour = timestamp.hour
    asia = 0 <= hour < 8
    london = 8 <= hour < 16
    newyork = 13 <= hour < 21
    return SessionLabels(asia=asia, london=london, newyork=newyork)
