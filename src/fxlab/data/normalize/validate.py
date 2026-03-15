"""Canonical data validation helpers."""

from __future__ import annotations

from collections.abc import Sequence

from fxlab.domain.bars import CanonicalBar


def validate_sorted_bars(bars: Sequence[CanonicalBar]) -> None:
    """Ensure bars are sorted ascending by timestamp."""
    timestamps = [bar.timestamp for bar in bars]
    if timestamps != sorted(timestamps):
        raise ValueError("canonical bars must be sorted ascending by timestamp")


def validate_unique_timestamps(bars: Sequence[CanonicalBar]) -> None:
    """Ensure bars are unique by timestamp within a canonical series."""
    timestamps = [bar.timestamp for bar in bars]
    if len(timestamps) != len(set(timestamps)):
        raise ValueError("canonical bars must not contain duplicate timestamps")
