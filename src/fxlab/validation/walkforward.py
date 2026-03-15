"""Walk-forward scheduling helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WalkForwardWindow:
    """One walk-forward train/validation window pair."""

    train_start: int
    train_end: int
    validation_start: int
    validation_end: int


def build_walkforward_schedule(
    *,
    total_rows: int,
    train_size: int,
    validation_size: int,
    step_size: int,
) -> tuple[WalkForwardWindow, ...]:
    """Build deterministic rolling walk-forward windows."""
    if min(total_rows, train_size, validation_size, step_size) <= 0:
        raise ValueError("schedule sizes must be positive")
    windows: list[WalkForwardWindow] = []
    train_start = 0
    while True:
        train_end = train_start + train_size
        validation_start = train_end
        validation_end = validation_start + validation_size
        if validation_end > total_rows:
            break
        windows.append(
            WalkForwardWindow(
                train_start=train_start,
                train_end=train_end,
                validation_start=validation_start,
                validation_end=validation_end,
            )
        )
        train_start += step_size
    if not windows:
        raise ValueError("schedule configuration yields no windows")
    return tuple(windows)
