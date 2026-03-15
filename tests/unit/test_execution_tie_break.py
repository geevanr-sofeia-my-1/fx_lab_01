"""Same-bar tie-break tests."""

from fxlab.execution.tie_break import resolve_same_bar_exit


def test_pessimistic_same_bar_policy_prefers_stop_loss() -> None:
    assert (
        resolve_same_bar_exit(stop_touched=True, target_touched=True, policy="pessimistic")
        == "stop_loss"
    )


def test_same_bar_policy_returns_single_touch_reason() -> None:
    assert resolve_same_bar_exit(stop_touched=False, target_touched=True) == "take_profit"
