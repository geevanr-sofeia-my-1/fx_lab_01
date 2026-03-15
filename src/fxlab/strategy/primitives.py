"""Primitive rule evaluation."""

from __future__ import annotations

from collections.abc import Sequence

from fxlab.strategy.schema import (
    CrossesAboveRule,
    CrossesBelowRule,
    FeatureRef,
    GreaterThanRule,
    LessThanRule,
    Operand,
)


def resolve_operand(
    operand: Operand,
    rows: Sequence[dict[str, object]],
    index: int,
) -> float | int | bool | None:
    """Resolve an operand against the current row."""
    if operand.kind == "value":
        return operand.value
    return resolve_feature(operand, rows, index)


def resolve_feature(
    feature: FeatureRef,
    rows: Sequence[dict[str, object]],
    index: int,
) -> float | int | bool | None:
    """Resolve a feature reference against the current row."""
    value = rows[index].get(feature.name)
    return value if value is None else value  # keep explicit for type narrowing symmetry


def eval_greater_than(
    rule: GreaterThanRule,
    rows: Sequence[dict[str, object]],
    index: int,
) -> bool:
    """Evaluate a greater-than predicate."""
    left = resolve_feature(rule.left, rows, index)
    right = resolve_operand(rule.right, rows, index)
    if left is None or right is None:
        return False
    return bool(left > right)


def eval_less_than(
    rule: LessThanRule,
    rows: Sequence[dict[str, object]],
    index: int,
) -> bool:
    """Evaluate a less-than predicate."""
    left = resolve_feature(rule.left, rows, index)
    right = resolve_operand(rule.right, rows, index)
    if left is None or right is None:
        return False
    return bool(left < right)


def eval_crosses_above(
    rule: CrossesAboveRule,
    rows: Sequence[dict[str, object]],
    index: int,
) -> bool:
    """Evaluate a crosses-above predicate."""
    if index == 0:
        return False
    prev_left = resolve_feature(rule.left, rows, index - 1)
    prev_right = resolve_operand(rule.right, rows, index - 1)
    curr_left = resolve_feature(rule.left, rows, index)
    curr_right = resolve_operand(rule.right, rows, index)
    if None in (prev_left, prev_right, curr_left, curr_right):
        return False
    return bool(prev_left <= prev_right and curr_left > curr_right)


def eval_crosses_below(
    rule: CrossesBelowRule,
    rows: Sequence[dict[str, object]],
    index: int,
) -> bool:
    """Evaluate a crosses-below predicate."""
    if index == 0:
        return False
    prev_left = resolve_feature(rule.left, rows, index - 1)
    prev_right = resolve_operand(rule.right, rows, index - 1)
    curr_left = resolve_feature(rule.left, rows, index)
    curr_right = resolve_operand(rule.right, rows, index)
    if None in (prev_left, prev_right, curr_left, curr_right):
        return False
    return bool(prev_left >= prev_right and curr_left < curr_right)
