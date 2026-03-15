"""Minimal experiment ranking helpers."""

from __future__ import annotations

from collections.abc import Sequence

from fxlab.experiments.artifacts import RunSummary


def build_leaderboard(run_summaries: Sequence[RunSummary]) -> tuple[RunSummary, ...]:
    """Sort run summaries by deterministic composite score."""
    return tuple(
        sorted(
            run_summaries,
            key=lambda summary: (
                summary.composite_score,
                summary.net_return,
                summary.profit_factor,
                -summary.max_drawdown,
                summary.candidate_id,
            ),
            reverse=True,
        )
    )
