"""Portfolio constraint tests."""

import pytest

from fxlab.domain.account import AccountState
from fxlab.portfolio.constraints import can_open_position


def test_can_open_position_respects_max_open_positions() -> None:
    account = AccountState(cash=500.0, equity=500.0, open_positions=0)
    assert can_open_position(account, max_open_positions=1) is True

    full_account = AccountState(cash=500.0, equity=500.0, open_positions=1)
    assert can_open_position(full_account, max_open_positions=1) is False


def test_can_open_position_rejects_invalid_maximum() -> None:
    account = AccountState(cash=500.0, equity=500.0, open_positions=0)
    with pytest.raises(ValueError):
        can_open_position(account, max_open_positions=0)
