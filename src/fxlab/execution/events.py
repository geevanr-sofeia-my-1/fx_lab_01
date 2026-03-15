"""Execution event objects."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FillEvent:
    """A concrete fill event."""

    timestamp: str
    price: float
    reason: str
