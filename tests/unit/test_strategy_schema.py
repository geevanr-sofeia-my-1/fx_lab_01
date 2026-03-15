"""Strategy DSL schema tests."""

import pytest
from pydantic import ValidationError

from fxlab.strategy.schema import StrategyDefinition


def test_strategy_definition_validates_nested_rules() -> None:
    strategy = StrategyDefinition.model_validate(
        {
            "name": "ema_rsi_pullback",
            "pair_universe": ["EURUSD"],
            "timeframe": "1H",
            "regime_filter": {
                "type": "greater_than",
                "left": {"kind": "feature", "name": "close"},
                "right": {"kind": "feature", "name": "ema_length_3"},
            },
            "entry_trigger_rule": {
                "type": "crosses_above",
                "left": {"kind": "feature", "name": "rsi_length_3"},
                "right": {"kind": "value", "value": 50},
            },
        }
    )

    assert strategy.name == "ema_rsi_pullback"


def test_strategy_definition_rejects_missing_trigger() -> None:
    with pytest.raises(ValidationError):
        StrategyDefinition.model_validate(
            {
                "name": "invalid",
                "pair_universe": ["EURUSD"],
                "timeframe": "1H",
            }
        )
