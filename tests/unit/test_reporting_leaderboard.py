"""Leaderboard report tests."""

from fxlab.experiments.artifacts import RunSummary
from fxlab.reporting.leaderboard import leaderboard_rows


def test_leaderboard_rows_are_ranked_and_serializable() -> None:
    rows = leaderboard_rows(
        (
            RunSummary(
                run_id="run-1",
                candidate_id="a",
                net_return=0.1,
                max_drawdown=-0.05,
                profit_factor=1.4,
                trade_count=40,
            ),
            RunSummary(
                run_id="run-2",
                candidate_id="b",
                net_return=0.05,
                max_drawdown=-0.05,
                profit_factor=1.1,
                trade_count=40,
            ),
        )
    )

    assert rows[0]["rank"] == 1
    assert rows[0]["run_id"] == "run-1"
    assert rows[1]["rank"] == 2
