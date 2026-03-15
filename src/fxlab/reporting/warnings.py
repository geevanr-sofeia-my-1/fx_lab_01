"""Warning flag helpers for experiment outputs."""

from __future__ import annotations

from collections.abc import Sequence

from fxlab.experiments.artifacts import RunSummary


def warning_flags_for_run(
    summary: RunSummary,
    *,
    minimum_trade_count: int = 30,
    max_drawdown_limit: float = -0.25,
) -> tuple[str, ...]:
    """Return human-readable warning flags for a run summary."""
    warnings: list[str] = []
    if summary.trade_count < minimum_trade_count:
        warnings.append("low_trade_count")
    if summary.max_drawdown < max_drawdown_limit:
        warnings.append("drawdown_breach")
    if summary.profit_factor < 1.0:
        warnings.append("subunit_profit_factor")
    return tuple(warnings)


def any_warnings(run_summaries: Sequence[RunSummary], *, minimum_trade_count: int = 30) -> bool:
    """Return whether any run in a batch is warning-flagged."""
    return any(
        warning_flags_for_run(item, minimum_trade_count=minimum_trade_count)
        for item in run_summaries
    )
