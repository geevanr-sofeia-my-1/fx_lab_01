"""Deterministic Monte Carlo helpers."""

from __future__ import annotations

import random
from collections.abc import Sequence


def monte_carlo_trade_pnl(
    trade_pnls: Sequence[float],
    *,
    seed: int,
    iterations: int,
) -> tuple[tuple[float, ...], ...]:
    """Generate deterministic trade-order reshuffles."""
    if iterations <= 0:
        raise ValueError("iterations must be positive")
    rng = random.Random(seed)
    outputs: list[tuple[float, ...]] = []
    base = list(trade_pnls)
    for _ in range(iterations):
        sample = base[:]
        rng.shuffle(sample)
        outputs.append(tuple(sample))
    return tuple(outputs)
