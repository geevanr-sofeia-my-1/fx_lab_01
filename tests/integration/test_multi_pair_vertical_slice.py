"""Multi-pair vertical slice integration test."""

import shutil
import uuid
from datetime import UTC, datetime
from pathlib import Path

from fxlab.config.dataset import DatasetRequestConfig
from fxlab.config.execution import ExecutionConfig
from fxlab.config.experiment import ExperimentRunConfig
from fxlab.config.risk import RiskConfig
from fxlab.config.strategy import StrategyConfig
from fxlab.config.validation import ValidationPlanConfig
from fxlab.domain.enums import Pair
from fxlab.experiments.multi_pair import run_multi_pair_vertical_slice
from fxlab.strategy.schema import (
    FeatureRef,
    GreaterThanRule,
    StrategyDefinition,
    ValueRef,
)


def _fetcher(*_args: object) -> bytes:
    return "\n".join(
        [
            "timestamp,open,high,low,close,volume",
            "2024-01-01T00:00:00Z,1,1.2,0.9,1,100",
            "2024-01-01T01:00:00Z,2,2.2,1.9,2,100",
            "2024-01-01T02:00:00Z,3,3.2,2.9,3,100",
            "2024-01-01T03:00:00Z,4,4.2,3.9,4,100",
            "2024-01-01T04:00:00Z,5,8.0,4.8,7,100",
            "2024-01-01T05:00:00Z,6,8.0,5.8,7,100",
        ]
    ).encode()


def _config() -> ExperimentRunConfig:
    return ExperimentRunConfig(
        name="vertical_slice_demo",
        random_seed=7,
        dataset=DatasetRequestConfig(
            pair="EURUSD",
            timeframe="1H",
            start=datetime(2024, 1, 1, tzinfo=UTC),
            end=datetime(2024, 1, 1, 6, tzinfo=UTC),
            price_basis="mid",
        ),
        strategy=StrategyConfig(
            name="vertical_slice_demo",
            pair_universe=("EURUSD",),
            timeframe="1H",
            feature_set=("ema_length_3", "rsi_length_3", "atr_length_3"),
        ),
        execution=ExecutionConfig(spread_pips=0.0, slippage_pips=0.0),
        risk=RiskConfig(starting_capital=500.0, risk_fraction=0.01, max_open_positions=1),
        validation=ValidationPlanConfig(minimum_trade_count=1),
    )


def _strategy() -> StrategyDefinition:
    return StrategyDefinition(
        name="vertical_slice_demo",
        pair_universe=("EURUSD",),
        timeframe="1H",
        regime_filter=GreaterThanRule(
            left=FeatureRef(name="close"),
            right=FeatureRef(name="ema_length_3"),
        ),
        entry_trigger_rule=GreaterThanRule(
            left=FeatureRef(name="close"),
            right=ValueRef(value=3.5),
        ),
    )


def test_multi_pair_vertical_slice_aggregates_pair_results() -> None:
    scratch = Path("artifacts") / "cache" / f"test_multi_pair_{uuid.uuid4().hex}"
    scratch.mkdir(parents=True, exist_ok=True)
    try:
        result = run_multi_pair_vertical_slice(
            config=_config(),
            strategy=_strategy(),
            pairs=(Pair.EURUSD, Pair.GBPUSD),
            fetcher=_fetcher,
            repo_root=scratch,
        )

        assert len(result.pair_results) == 2
        assert result.aggregate_summary["pair_count"] == 2
        assert result.aggregate_summary["pairs"] == ["EURUSD", "GBPUSD"]
        assert result.aggregate_summary["total_trade_count"] >= 2
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
