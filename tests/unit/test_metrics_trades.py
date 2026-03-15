"""Trade metric tests."""

from fxlab.domain.trades import Trade
from fxlab.metrics.trades import expectancy, profit_factor, win_rate


def _trades() -> tuple[Trade, ...]:
    return (
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


def test_win_rate_expectancy_and_profit_factor() -> None:
    trades = _trades()
    assert win_rate(trades) == 0.5
    assert expectancy(trades) == 0.5
    assert profit_factor(trades) == 2.0
