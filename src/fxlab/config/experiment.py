"""Experiment configuration models."""

from __future__ import annotations

from fxlab.config.dataset import DatasetRequestConfig
from fxlab.config.execution import ExecutionConfig
from fxlab.config.risk import RiskConfig
from fxlab.config.schema_base import FXLabBaseModel
from fxlab.config.strategy import StrategyConfig
from fxlab.config.validation import ValidationPlanConfig


class ExperimentRunConfig(FXLabBaseModel):
    """Top-level experiment definition."""

    schema_version: str = "1"
    name: str
    random_seed: int
    dataset: DatasetRequestConfig
    strategy: StrategyConfig
    execution: ExecutionConfig
    risk: RiskConfig
    validation: ValidationPlanConfig
