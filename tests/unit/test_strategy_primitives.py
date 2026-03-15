"""Primitive strategy rule tests."""

from fxlab.strategy.primitives import (
    eval_crosses_above,
    eval_crosses_below,
    eval_greater_than,
    eval_less_than,
)
from fxlab.strategy.schema import (
    CrossesAboveRule,
    CrossesBelowRule,
    FeatureRef,
    GreaterThanRule,
    LessThanRule,
    ValueRef,
)


def _rows() -> tuple[dict[str, object], ...]:
    return (
        {"timestamp": "t0", "a": 1.0, "b": 2.0},
        {"timestamp": "t1", "a": 3.0, "b": 2.0},
        {"timestamp": "t2", "a": 1.0, "b": 2.0},
    )


def test_greater_and_less_than_rules() -> None:
    rows = _rows()
    assert eval_greater_than(
        GreaterThanRule(left=FeatureRef(name="a"), right=ValueRef(value=2.5)),
        rows,
        1,
    )
    assert eval_less_than(
        LessThanRule(left=FeatureRef(name="a"), right=FeatureRef(name="b")),
        rows,
        0,
    )


def test_cross_rules_detect_directional_crosses() -> None:
    rows = _rows()
    assert eval_crosses_above(
        CrossesAboveRule(left=FeatureRef(name="a"), right=FeatureRef(name="b")),
        rows,
        1,
    )
    assert eval_crosses_below(
        CrossesBelowRule(left=FeatureRef(name="a"), right=FeatureRef(name="b")),
        rows,
        2,
    )
