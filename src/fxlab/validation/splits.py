"""Deterministic data split helpers."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class SplitWindow:
    """Half-open split window over an ordered sequence."""

    start_index: int
    end_index: int


def make_train_validation_test_split(
    rows: Sequence[object],
    *,
    train_fraction: float,
    validation_fraction: float,
    test_fraction: float,
) -> tuple[SplitWindow, SplitWindow, SplitWindow]:
    """Build deterministic train/validation/test windows."""
    if not rows:
        raise ValueError("rows must not be empty")
    total = len(rows)
    if round(train_fraction + validation_fraction + test_fraction, 10) != 1.0:
        raise ValueError("split fractions must sum to 1.0")

    train_end = int(total * train_fraction)
    validation_end = train_end + int(total * validation_fraction)
    if train_end <= 0 or validation_end <= train_end or validation_end >= total:
        raise ValueError("split fractions produce invalid boundaries")

    train = SplitWindow(0, train_end)
    validation = SplitWindow(train_end, validation_end)
    test = SplitWindow(validation_end, total)
    return train, validation, test
