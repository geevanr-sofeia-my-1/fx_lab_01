"""Regression tests for validation and selection leakage guards."""

from fxlab.experiments.artifacts import RunSummary
from fxlab.experiments.runner import build_leaderboard
from fxlab.validation.splits import make_train_validation_test_split


def test_split_windows_are_non_overlapping() -> None:
    train, validation, test = make_train_validation_test_split(
        list(range(20)),
        train_fraction=0.6,
        validation_fraction=0.2,
        test_fraction=0.2,
    )

    assert train.end_index <= validation.start_index
    assert validation.end_index <= test.start_index


def test_leaderboard_penalizes_low_trade_count_even_if_return_is_higher() -> None:
    leaderboard = build_leaderboard(
        (
            RunSummary(
                run_id="fragile",
                candidate_id="fragile",
                net_return=0.20,
                max_drawdown=-0.05,
                profit_factor=1.2,
                trade_count=5,
            ),
            RunSummary(
                run_id="stable",
                candidate_id="stable",
                net_return=0.15,
                max_drawdown=-0.05,
                profit_factor=1.2,
                trade_count=40,
            ),
        )
    )

    assert leaderboard[0].run_id == "stable"
