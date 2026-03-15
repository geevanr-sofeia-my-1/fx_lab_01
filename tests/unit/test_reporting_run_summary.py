"""Run summary report tests."""

from fxlab.experiments.artifacts import RunSummary
from fxlab.reporting.run_summary import build_run_summary


def test_build_run_summary_includes_composite_score_and_warnings() -> None:
    summary = RunSummary(
        run_id="run-1",
        candidate_id="ema__length_20",
        net_return=0.1,
        max_drawdown=-0.05,
        profit_factor=1.2,
        trade_count=10,
    )

    payload = build_run_summary(summary)

    assert payload["run_id"] == "run-1"
    assert "composite_score" in payload
    assert payload["warnings"] == ["low_trade_count"]
