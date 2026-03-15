"""Feature alignment and anti-leakage helpers."""

from __future__ import annotations

from collections.abc import Sequence


def shift_values(values: Sequence[float | None], periods: int = 1) -> tuple[float | None, ...]:
    """Shift values forward to enforce decision-time availability."""
    if periods < 0:
        raise ValueError("periods must be non-negative")
    if periods == 0:
        return tuple(values)
    prefix: tuple[float | None, ...] = tuple(None for _ in range(periods))
    return prefix + tuple(values[:-periods] if periods <= len(values) else ())


def rolling_mean(values: Sequence[float], window: int) -> tuple[float | None, ...]:
    """Compute a simple rolling mean with explicit warmup None values."""
    if window <= 0:
        raise ValueError("window must be positive")
    output: list[float | None] = []
    for index in range(len(values)):
        if index + 1 < window:
            output.append(None)
            continue
        chunk = values[index + 1 - window : index + 1]
        output.append(sum(chunk) / window)
    return tuple(output)
