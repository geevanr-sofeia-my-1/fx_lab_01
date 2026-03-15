"""Execution cost tests."""

from fxlab.execution.costs import apply_entry_costs, apply_exit_costs


def test_apply_entry_costs_for_long_position() -> None:
    assert apply_entry_costs(100.0, side="long", spread_pips=1.0, slippage_pips=0.5) == 101.5


def test_apply_exit_costs_for_long_position() -> None:
    assert apply_exit_costs(110.0, side="long", slippage_pips=0.5) == 109.5
