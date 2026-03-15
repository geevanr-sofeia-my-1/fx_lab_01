"""Portfolio accounting tests."""

from fxlab.domain.trades import Trade
from fxlab.portfolio.accounting import apply_trade_to_account, initialize_account


def test_initialize_account_sets_cash_and_equity() -> None:
    account = initialize_account(500.0)
    assert account.cash == 500.0
    assert account.equity == 500.0


def test_apply_trade_to_account_updates_realized_pnl() -> None:
    account = initialize_account(500.0)
    trade = Trade(
        entry_timestamp="t1",
        exit_timestamp="t2",
        side="long",
        entry_price=100.0,
        exit_price=105.0,
        size=1.0,
        pnl=5.0,
        exit_reason="take_profit",
    )

    updated = apply_trade_to_account(account, trade)

    assert updated.cash == 505.0
    assert updated.equity == 505.0
    assert updated.realized_pnl == 5.0
