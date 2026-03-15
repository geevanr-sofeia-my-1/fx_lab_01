"""Multi-pair vertical slice helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from fxlab.config.experiment import ExperimentRunConfig
from fxlab.data.providers.dukascopy import Fetcher
from fxlab.domain.enums import Pair
from fxlab.experiments.pipeline import VerticalSliceResult, run_vertical_slice
from fxlab.strategy.schema import StrategyDefinition


@dataclass(frozen=True)
class MultiPairResult:
    """Aggregate output for a multi-pair vertical slice."""

    pair_results: tuple[VerticalSliceResult, ...]
    aggregate_summary: dict[str, object]


def run_multi_pair_vertical_slice(
    *,
    config: ExperimentRunConfig,
    strategy: StrategyDefinition,
    pairs: tuple[Pair, ...],
    fetcher: Fetcher,
    repo_root: Path | None = None,
) -> MultiPairResult:
    """Run the vertical slice once per pair and aggregate results."""
    results: list[VerticalSliceResult] = []
    for pair in pairs:
        pair_config = config.model_copy(
            update={
                "dataset": config.dataset.model_copy(update={"pair": pair}),
                "strategy": config.strategy.model_copy(update={"pair_universe": (pair,)}),
            }
        )
        pair_strategy = strategy.model_copy(update={"pair_universe": (pair,)})
        results.append(
            run_vertical_slice(
                config=pair_config,
                strategy=pair_strategy,
                fetcher=fetcher,
                repo_root=repo_root,
            )
        )

    net_returns = [float(result.summary["net_return"]) for result in results]
    trade_counts = [int(result.summary["trade_count"]) for result in results]
    aggregate = {
        "pair_count": len(results),
        "pairs": [pair for pair in pairs],
        "average_net_return": sum(net_returns) / len(net_returns) if net_returns else 0.0,
        "total_trade_count": sum(trade_counts),
    }
    return MultiPairResult(pair_results=tuple(results), aggregate_summary=aggregate)
