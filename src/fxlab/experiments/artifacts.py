"""Experiment summary artifacts."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RunSummary:
    """Compact experiment result used for leaderboard ranking."""

    run_id: str
    candidate_id: str
    net_return: float
    max_drawdown: float
    profit_factor: float
    trade_count: int

    @property
    def composite_score(self) -> float:
        """Simple deterministic ranking score.

        Conservative baseline:
        - reward return
        - penalize drawdown magnitude
        - reward profit factor
        - penalize very low trade counts
        """
        trade_penalty = 0.0 if self.trade_count >= 30 else (30 - self.trade_count) / 100.0
        return self.net_return + self.profit_factor - abs(self.max_drawdown) - trade_penalty
