"""Config schema validation tests."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from fxlab.config.dataset import DatasetRequestConfig
from fxlab.config.execution import ExecutionConfig
from fxlab.config.experiment import ExperimentRunConfig
from fxlab.config.risk import RiskConfig
from fxlab.config.strategy import StrategyConfig
from fxlab.config.validation import ValidationPlanConfig


def test_dataset_request_config_validates() -> None:
    config = DatasetRequestConfig(
        pair="EURUSD",
        timeframe="1H",
        start=datetime(2024, 1, 1, tzinfo=UTC),
        end=datetime(2024, 2, 1, tzinfo=UTC),
        price_basis="mid",
    )
    assert config.provider == "dukascopy"


def test_dataset_request_config_rejects_bad_window() -> None:
    with pytest.raises(ValidationError):
        DatasetRequestConfig(
            pair="EURUSD",
            timeframe="1H",
            start=datetime(2024, 2, 1, tzinfo=UTC),
            end=datetime(2024, 1, 1, tzinfo=UTC),
            price_basis="mid",
        )


def test_strategy_config_serializes_deterministically() -> None:
    strategy = StrategyConfig(
        name="ema_rsi_baseline",
        pair_universe=("EURUSD",),
        timeframe="1H",
        feature_set=("ema_50", "rsi_14"),
    )
    assert strategy.model_dump(mode="json") == {
        "schema_version": "1",
        "name": "ema_rsi_baseline",
        "pair_universe": ["EURUSD"],
        "timeframe": "1H",
        "feature_set": ["ema_50", "rsi_14"],
        "regime_filters": [],
        "setup_rules": [],
        "entry_trigger_rules": [],
        "exit_rules": [],
        "tags": [],
    }


def test_experiment_run_config_composes_subschemas() -> None:
    config = ExperimentRunConfig(
        name="bootstrap_run",
        random_seed=7,
        dataset=DatasetRequestConfig(
            pair="EURUSD",
            timeframe="1H",
            start=datetime(2024, 1, 1, tzinfo=UTC),
            end=datetime(2024, 2, 1, tzinfo=UTC),
            price_basis="mid",
        ),
        strategy=StrategyConfig(
            name="ema_rsi_baseline",
            pair_universe=("EURUSD",),
            timeframe="1H",
        ),
        execution=ExecutionConfig(),
        risk=RiskConfig(),
        validation=ValidationPlanConfig(),
    )
    assert config.execution.entry_timing == "next_bar_open"
