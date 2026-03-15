"""Execution engine tests."""

from fxlab.execution.engine import execute_long_only_strategy


def test_next_bar_open_entry_and_take_profit_exit() -> None:
    rows = (
        {
            "timestamp": "t0",
            "open": 100.0,
            "high": 101.0,
            "low": 99.0,
            "close": 100.5,
            "entry_signal": True,
            "stop_loss": 98.0,
            "take_profit": 103.0,
        },
        {
            "timestamp": "t1",
            "open": 101.0,
            "high": 104.0,
            "low": 100.0,
            "close": 103.5,
            "entry_signal": False,
            "stop_loss": 98.0,
            "take_profit": 103.0,
        },
    )

    trades = execute_long_only_strategy(rows, spread_pips=1.0, slippage_pips=0.5)

    assert len(trades) == 1
    assert trades[0].entry_timestamp == "t1"
    assert trades[0].entry_price == 102.5
    assert trades[0].exit_reason == "take_profit"
    assert trades[0].exit_price == 102.5


def test_same_bar_stop_and_target_uses_pessimistic_resolution() -> None:
    rows = (
        {
            "timestamp": "t0",
            "open": 100.0,
            "high": 101.0,
            "low": 99.0,
            "close": 100.5,
            "entry_signal": True,
            "stop_loss": 98.0,
            "take_profit": 105.0,
        },
        {
            "timestamp": "t1",
            "open": 101.0,
            "high": 106.0,
            "low": 97.0,
            "close": 102.0,
            "entry_signal": False,
            "stop_loss": 98.0,
            "take_profit": 105.0,
        },
    )

    trades = execute_long_only_strategy(rows, spread_pips=0.0, slippage_pips=0.0)

    assert len(trades) == 1
    assert trades[0].exit_reason == "stop_loss"
    assert trades[0].exit_price == 98.0
