"""Portfolio equity helpers tests."""

from fxlab.domain.account import AccountState
from fxlab.portfolio.equity import equity_curve_from_account_states


def test_equity_curve_from_account_states_returns_ordered_equity_values() -> None:
    states = (
        AccountState(cash=500.0, equity=500.0),
        AccountState(cash=505.0, equity=505.0, realized_pnl=5.0),
    )
    assert equity_curve_from_account_states(states) == (500.0, 505.0)
