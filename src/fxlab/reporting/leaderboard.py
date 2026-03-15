"""Leaderboard report helpers."""

from __future__ import annotations

from collections.abc import Sequence

from fxlab.experiments.artifacts import RunSummary
from fxlab.experiments.runner import build_leaderboard
from fxlab.reporting.warnings import warning_flags_for_run


def leaderboard_rows(run_summaries: Sequence[RunSummary]) -> tuple[dict[str, object], ...]:
    """Build serializable leaderboard rows from run summaries."""
    ranked = build_leaderboard(run_summaries)
    rows: list[dict[str, object]] = []
    for rank, summary in enumerate(ranked, start=1):
        rows.append(
            {
                "rank": rank,
                "run_id": summary.run_id,
                "candidate_id": summary.candidate_id,
                "composite_score": summary.composite_score,
                "net_return": summary.net_return,
                "max_drawdown": summary.max_drawdown,
                "profit_factor": summary.profit_factor,
                "trade_count": summary.trade_count,
                "warnings": list(warning_flags_for_run(summary)),
            }
        )
    return tuple(rows)
