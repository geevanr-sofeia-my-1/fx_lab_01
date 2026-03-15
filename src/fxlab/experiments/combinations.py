"""Controlled multi-indicator combination generation."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations


@dataclass(frozen=True)
class IndicatorSpec:
    """One indicator candidate with an assigned strategy role."""

    candidate_id: str
    role: str


@dataclass(frozen=True)
class CombinationCandidate:
    """A bounded, role-aware combination candidate."""

    candidate_id: str
    members: tuple[IndicatorSpec, ...]


def generate_two_indicator_combinations(
    indicators: tuple[IndicatorSpec, ...],
) -> tuple[CombinationCandidate, ...]:
    """Generate role-distinct 2-indicator combinations."""
    candidates: list[CombinationCandidate] = []
    for left, right in combinations(indicators, 2):
        if left.role == right.role:
            continue
        members = tuple(sorted((left, right), key=lambda item: item.candidate_id))
        candidate_id = "__".join(member.candidate_id for member in members)
        candidates.append(CombinationCandidate(candidate_id=candidate_id, members=members))
    return tuple(candidates)


def generate_three_indicator_combinations(
    indicators: tuple[IndicatorSpec, ...],
) -> tuple[CombinationCandidate, ...]:
    """Generate role-distinct 3-indicator combinations.

    The current conservative rule requires three distinct roles.
    """
    candidates: list[CombinationCandidate] = []
    for first, second, third in combinations(indicators, 3):
        roles = {first.role, second.role, third.role}
        if len(roles) != 3:
            continue
        members = tuple(
            sorted((first, second, third), key=lambda item: item.candidate_id)
        )
        candidate_id = "__".join(member.candidate_id for member in members)
        candidates.append(CombinationCandidate(candidate_id=candidate_id, members=members))
    return tuple(candidates)
