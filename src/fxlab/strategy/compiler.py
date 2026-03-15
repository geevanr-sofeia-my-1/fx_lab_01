"""Strategy signal compilation and evaluation."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from fxlab.strategy.composition import evaluate_rule_series
from fxlab.strategy.schema import StrategyDefinition


@dataclass(frozen=True)
class CompiledSignalRow:
    """Compiled strategy signal state for one timestamp."""

    timestamp: str
    regime_ok: bool
    setup_ok: bool
    trigger_ok: bool
    raw_entry_signal: bool
    entry_signal: bool


def shift_bool_series(values: Sequence[bool], periods: int = 1) -> tuple[bool, ...]:
    """Shift boolean signals forward with False warmup."""
    if periods < 0:
        raise ValueError("periods must be non-negative")
    if periods == 0:
        return tuple(values)
    return tuple(False for _ in range(periods)) + tuple(values[:-periods])


def evaluate_strategy(
    strategy: StrategyDefinition,
    rows: Sequence[dict[str, object]],
) -> tuple[CompiledSignalRow, ...]:
    """Evaluate a minimal strategy definition over feature rows."""
    regime = (
        evaluate_rule_series(strategy.regime_filter, rows)
        if strategy.regime_filter is not None
        else tuple(True for _ in rows)
    )
    setup = (
        evaluate_rule_series(strategy.setup_rule, rows)
        if strategy.setup_rule is not None
        else tuple(True for _ in rows)
    )
    trigger = evaluate_rule_series(strategy.entry_trigger_rule, rows)
    raw_entry = tuple(regime[i] and setup[i] and trigger[i] for i in range(len(rows)))
    entry = shift_bool_series(raw_entry) if strategy.shift_entry_signals else raw_entry
    return tuple(
        CompiledSignalRow(
            timestamp=str(rows[index]["timestamp"]),
            regime_ok=regime[index],
            setup_ok=setup[index],
            trigger_ok=trigger[index],
            raw_entry_signal=raw_entry[index],
            entry_signal=entry[index],
        )
        for index in range(len(rows))
    )
