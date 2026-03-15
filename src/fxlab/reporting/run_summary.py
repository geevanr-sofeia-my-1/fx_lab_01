"""Run summary rendering helpers."""

from __future__ import annotations

from fxlab.experiments.artifacts import RunSummary
from fxlab.reporting.warnings import warning_flags_for_run


def build_run_summary(summary: RunSummary) -> dict[str, object]:
    """Build a compact serializable run summary payload."""
    warnings = warning_flags_for_run(summary)
    return {
        "run_id": summary.run_id,
        "candidate_id": summary.candidate_id,
        "net_return": summary.net_return,
        "max_drawdown": summary.max_drawdown,
        "profit_factor": summary.profit_factor,
        "trade_count": summary.trade_count,
        "composite_score": summary.composite_score,
        "warnings": list(warnings),
    }
