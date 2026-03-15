"""Example config validation tests."""

from pathlib import Path

import yaml

from fxlab.config.experiment import ExperimentRunConfig
from fxlab.config.validation import ValidationPlanConfig
from fxlab.strategy.schema import StrategyDefinition


def test_example_experiment_config_validates() -> None:
    payload = yaml.safe_load(
        Path("configs/experiments/vertical_slice_demo.yaml").read_text(encoding="utf-8")
    )
    config = ExperimentRunConfig.model_validate(payload)
    assert config.name == "vertical_slice_demo"


def test_example_strategy_config_validates() -> None:
    payload = yaml.safe_load(
        Path("configs/strategies/vertical_slice_strategy.yaml").read_text(encoding="utf-8")
    )
    strategy = StrategyDefinition.model_validate(payload)
    assert strategy.name == "vertical_slice_demo"


def test_example_validation_config_validates() -> None:
    payload = yaml.safe_load(
        Path("configs/validation/standard_walkforward.yaml").read_text(encoding="utf-8")
    )
    validation = ValidationPlanConfig.model_validate(payload)
    assert validation.minimum_trade_count == 30
