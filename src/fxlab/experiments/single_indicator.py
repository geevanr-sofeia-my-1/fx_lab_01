"""Single-indicator experiment enumeration."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True)
class SingleIndicatorCandidate:
    """One reproducible single-indicator experiment candidate."""

    indicator_name: str
    params: tuple[tuple[str, object], ...]
    candidate_id: str


def enumerate_single_indicator_candidates(
    parameter_grid: dict[str, dict[str, tuple[object, ...]]],
) -> tuple[SingleIndicatorCandidate, ...]:
    """Enumerate candidates deterministically from an indicator parameter grid.

    Example input:
    {
        "ema": {"length": (20, 50)},
        "rsi": {"length": (7, 14)},
    }
    """
    candidates: list[SingleIndicatorCandidate] = []
    for indicator_name in sorted(parameter_grid):
        grid = parameter_grid[indicator_name]
        param_names = sorted(grid)
        value_lists = [grid[name] for name in param_names]
        for combination in product(*value_lists):
            params = tuple(
                (name, value)
                for name, value in zip(param_names, combination, strict=False)
            )
            suffix = "_".join(f"{name}_{value}" for name, value in params)
            candidate_id = f"{indicator_name}__{suffix}" if suffix else indicator_name
            candidates.append(
                SingleIndicatorCandidate(
                    indicator_name=indicator_name,
                    params=params,
                    candidate_id=candidate_id,
                )
            )
    return tuple(candidates)
