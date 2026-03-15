"""Reporting warning flag tests."""

from fxlab.experiments.artifacts import RunSummary
from fxlab.reporting.warnings import warning_flags_for_run


def test_warning_flags_cover_trade_count_drawdown_and_profit_factor() -> None:
    summary = RunSummary(
        run_id="run-1",
        candidate_id="ema__length_20",
        net_return=-0.1,
        max_drawdown=-0.3,
        profit_factor=0.8,
        trade_count=10,
    )

    assert warning_flags_for_run(summary) == (
        "low_trade_count",
        "drawdown_breach",
        "subunit_profit_factor",
    )
