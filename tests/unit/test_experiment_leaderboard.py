"""Experiment leaderboard tests."""

from fxlab.experiments.artifacts import RunSummary
from fxlab.experiments.runner import build_leaderboard


def test_build_leaderboard_sorts_by_composite_score() -> None:
    leaderboard = build_leaderboard(
        (
            RunSummary(
                run_id="run-1",
                candidate_id="ema__length_20",
                net_return=0.10,
                max_drawdown=-0.05,
                profit_factor=1.5,
                trade_count=40,
            ),
            RunSummary(
                run_id="run-2",
                candidate_id="rsi__length_14",
                net_return=0.08,
                max_drawdown=-0.20,
                profit_factor=1.1,
                trade_count=40,
            ),
        )
    )

    assert leaderboard[0].run_id == "run-1"


def test_low_trade_count_is_penalized() -> None:
    leaderboard = build_leaderboard(
        (
            RunSummary(
                run_id="run-1",
                candidate_id="a",
                net_return=0.10,
                max_drawdown=-0.05,
                profit_factor=1.2,
                trade_count=5,
            ),
            RunSummary(
                run_id="run-2",
                candidate_id="b",
                net_return=0.09,
                max_drawdown=-0.05,
                profit_factor=1.2,
                trade_count=40,
            ),
        )
    )

    assert leaderboard[0].run_id == "run-2"
