"""Strategy composition tests."""

from fxlab.strategy.composition import evaluate_rule, evaluate_rule_series
from fxlab.strategy.schema import (
    AllOfRule,
    AnyOfRule,
    FeatureRef,
    GreaterThanRule,
    NotRule,
    ValueRef,
)


def _rows() -> tuple[dict[str, object], ...]:
    return (
        {"timestamp": "t0", "x": 1.0, "y": 3.0},
        {"timestamp": "t1", "x": 4.0, "y": 2.0},
    )


def test_all_of_and_any_of_rules() -> None:
    rows = _rows()
    gt_x = GreaterThanRule(left=FeatureRef(name="x"), right=ValueRef(value=2))
    gt_y = GreaterThanRule(left=FeatureRef(name="y"), right=ValueRef(value=1))
    assert evaluate_rule(AllOfRule(conditions=(gt_x, gt_y)), rows, 1)
    assert evaluate_rule(AnyOfRule(conditions=(gt_x, gt_y)), rows, 0)


def test_not_rule_and_series() -> None:
    rows = _rows()
    gt_x = GreaterThanRule(left=FeatureRef(name="x"), right=ValueRef(value=2))
    not_gt_x = NotRule(condition=gt_x)
    assert evaluate_rule(not_gt_x, rows, 0)
    assert evaluate_rule_series(gt_x, rows) == (False, True)
