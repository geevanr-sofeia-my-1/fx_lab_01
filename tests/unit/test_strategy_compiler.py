"""Strategy compiler tests."""

from fxlab.strategy.compiler import evaluate_strategy
from fxlab.strategy.schema import (
    CrossesAboveRule,
    FeatureRef,
    GreaterThanRule,
    StrategyDefinition,
    ValueRef,
)


def _rows() -> tuple[dict[str, object], ...]:
    return (
        {"timestamp": "t0", "close": 1.0, "ema_length_3": 0.5, "rsi_length_3": 45.0},
        {"timestamp": "t1", "close": 2.0, "ema_length_3": 1.0, "rsi_length_3": 55.0},
        {"timestamp": "t2", "close": 2.0, "ema_length_3": 1.5, "rsi_length_3": 60.0},
    )


def test_strategy_evaluation_shifts_entry_signals_by_default() -> None:
    strategy = StrategyDefinition(
        name="demo",
        pair_universe=("EURUSD",),
        timeframe="1H",
        regime_filter=GreaterThanRule(
            left=FeatureRef(name="close"),
            right=FeatureRef(name="ema_length_3"),
        ),
        entry_trigger_rule=CrossesAboveRule(
            left=FeatureRef(name="rsi_length_3"),
            right=ValueRef(value=50),
        ),
    )

    result = evaluate_strategy(strategy, _rows())

    assert [row.raw_entry_signal for row in result] == [False, True, False]
    assert [row.entry_signal for row in result] == [False, False, True]


def test_strategy_evaluation_can_disable_shift() -> None:
    strategy = StrategyDefinition(
        name="demo_no_shift",
        pair_universe=("EURUSD",),
        timeframe="1H",
        entry_trigger_rule=GreaterThanRule(
            left=FeatureRef(name="close"),
            right=ValueRef(value=1.5),
        ),
        shift_entry_signals=False,
    )

    result = evaluate_strategy(strategy, _rows())

    assert [row.entry_signal for row in result] == [False, True, True]
