"""Grouped metric helper tests."""

from fxlab.domain.trades import Trade
from fxlab.metrics.grouped import group_trades_by_exit_reason


def test_group_trades_by_exit_reason() -> None:
    trades = (
        Trade(
            entry_timestamp="t1",
            exit_timestamp="t2",
            side="long",
            entry_price=100.0,
            exit_price=102.0,
            size=1.0,
            pnl=2.0,
            exit_reason="take_profit",
        ),
        Trade(
            entry_timestamp="t3",
            exit_timestamp="t4",
            side="long",
            entry_price=100.0,
            exit_price=99.0,
            size=1.0,
            pnl=-1.0,
            exit_reason="stop_loss",
        ),
    )

    grouped = group_trades_by_exit_reason(trades)

    assert tuple(grouped) == ("take_profit", "stop_loss")
    assert len(grouped["take_profit"]) == 1
