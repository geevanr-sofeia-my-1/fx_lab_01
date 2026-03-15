"""Boolean rule composition."""

from __future__ import annotations

from collections.abc import Sequence

from fxlab.strategy.primitives import (
    eval_crosses_above,
    eval_crosses_below,
    eval_greater_than,
    eval_less_than,
)
from fxlab.strategy.schema import (
    AllOfRule,
    AnyOfRule,
    CrossesAboveRule,
    CrossesBelowRule,
    GreaterThanRule,
    LessThanRule,
    NotRule,
    RuleExpression,
)


def evaluate_rule(
    rule: RuleExpression,
    rows: Sequence[dict[str, object]],
    index: int,
) -> bool:
    """Evaluate a rule expression against one row index."""
    if isinstance(rule, GreaterThanRule):
        return eval_greater_than(rule, rows, index)
    if isinstance(rule, LessThanRule):
        return eval_less_than(rule, rows, index)
    if isinstance(rule, CrossesAboveRule):
        return eval_crosses_above(rule, rows, index)
    if isinstance(rule, CrossesBelowRule):
        return eval_crosses_below(rule, rows, index)
    if isinstance(rule, AllOfRule):
        return all(evaluate_rule(condition, rows, index) for condition in rule.conditions)
    if isinstance(rule, AnyOfRule):
        return any(evaluate_rule(condition, rows, index) for condition in rule.conditions)
    if isinstance(rule, NotRule):
        return not evaluate_rule(rule.condition, rows, index)
    raise TypeError(f"unsupported rule type: {type(rule)!r}")


def evaluate_rule_series(
    rule: RuleExpression,
    rows: Sequence[dict[str, object]],
) -> tuple[bool, ...]:
    """Evaluate a rule expression over all rows."""
    return tuple(evaluate_rule(rule, rows, index) for index in range(len(rows)))
