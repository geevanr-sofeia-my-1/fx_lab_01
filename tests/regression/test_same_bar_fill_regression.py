"""Regression tests for conservative same-bar execution behavior."""

from fxlab.execution.engine import execute_long_only_strategy


def test_next_bar_entry_prevents_same_bar_entry_exit_fantasy() -> None:
    rows = (
        {
            "timestamp": "t0",
            "open": 100.0,
            "high": 110.0,
            "low": 90.0,
            "close": 100.0,
            "entry_signal": True,
            "stop_loss": 95.0,
            "take_profit": 105.0,
        },
    )

    trades = execute_long_only_strategy(rows, spread_pips=0.0, slippage_pips=0.0)

    assert trades == ()


def test_same_bar_stop_and_target_is_pessimistic() -> None:
    rows = (
        {
            "timestamp": "t0",
            "open": 100.0,
            "high": 101.0,
            "low": 99.0,
            "close": 100.0,
            "entry_signal": True,
            "stop_loss": 98.0,
            "take_profit": 105.0,
        },
        {
            "timestamp": "t1",
            "open": 100.0,
            "high": 106.0,
            "low": 97.0,
            "close": 101.0,
            "entry_signal": False,
            "stop_loss": 98.0,
            "take_profit": 105.0,
        },
    )

    trades = execute_long_only_strategy(rows, spread_pips=0.0, slippage_pips=0.0)

    assert len(trades) == 1
    assert trades[0].exit_reason == "stop_loss"
