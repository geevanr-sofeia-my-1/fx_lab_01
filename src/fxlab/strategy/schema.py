"""Typed strategy DSL schema."""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field

from fxlab.config.schema_base import FXLabBaseModel
from fxlab.domain.enums import Pair, Timeframe


class FeatureRef(FXLabBaseModel):
    """Reference a feature column by name."""

    kind: Literal["feature"] = "feature"
    name: str


class ValueRef(FXLabBaseModel):
    """Embed a literal comparison value."""

    kind: Literal["value"] = "value"
    value: float | int | bool


Operand = Annotated[FeatureRef | ValueRef, Field(discriminator="kind")]


class GreaterThanRule(FXLabBaseModel):
    """Check whether one operand is greater than another."""

    type: Literal["greater_than"] = "greater_than"
    left: FeatureRef
    right: Operand


class LessThanRule(FXLabBaseModel):
    """Check whether one operand is less than another."""

    type: Literal["less_than"] = "less_than"
    left: FeatureRef
    right: Operand


class CrossesAboveRule(FXLabBaseModel):
    """Detect a crossing from at/below to above."""

    type: Literal["crosses_above"] = "crosses_above"
    left: FeatureRef
    right: Operand


class CrossesBelowRule(FXLabBaseModel):
    """Detect a crossing from at/above to below."""

    type: Literal["crosses_below"] = "crosses_below"
    left: FeatureRef
    right: Operand


class AllOfRule(FXLabBaseModel):
    """Logical AND composition."""

    type: Literal["all_of"] = "all_of"
    conditions: tuple[RuleExpression, ...]


class AnyOfRule(FXLabBaseModel):
    """Logical OR composition."""

    type: Literal["any_of"] = "any_of"
    conditions: tuple[RuleExpression, ...]


class NotRule(FXLabBaseModel):
    """Logical NOT composition."""

    type: Literal["not"] = "not"
    condition: RuleExpression


RuleExpression = Annotated[
    GreaterThanRule
    | LessThanRule
    | CrossesAboveRule
    | CrossesBelowRule
    | AllOfRule
    | AnyOfRule
    | NotRule,
    Field(discriminator="type"),
]


class StrategyDefinition(FXLabBaseModel):
    """Minimal config-driven strategy definition."""

    schema_version: str = "1"
    name: str
    pair_universe: tuple[Pair, ...]
    timeframe: Timeframe
    feature_set: tuple[str, ...] = ()
    regime_filter: RuleExpression | None = None
    setup_rule: RuleExpression | None = None
    entry_trigger_rule: RuleExpression
    shift_entry_signals: bool = True


AllOfRule.model_rebuild()
AnyOfRule.model_rebuild()
NotRule.model_rebuild()
