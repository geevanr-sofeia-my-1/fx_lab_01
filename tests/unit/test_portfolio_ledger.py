"""Portfolio ledger tests."""

from fxlab.domain.trades import Trade
from fxlab.portfolio.ledger import total_realized_pnl


def test_total_realized_pnl_sums_trade_results() -> None:
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
    assert total_realized_pnl(trades) == 1.0
