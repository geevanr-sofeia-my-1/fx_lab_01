"""Strategy configuration models."""

from __future__ import annotations

from fxlab.config.schema_base import FXLabBaseModel
from fxlab.domain.enums import Pair, Timeframe


class StrategyConfig(FXLabBaseModel):
    """Minimal config-defined strategy contract."""

    schema_version: str = "1"
    name: str
    pair_universe: tuple[Pair, ...]
    timeframe: Timeframe
    feature_set: tuple[str, ...] = ()
    regime_filters: tuple[str, ...] = ()
    setup_rules: tuple[str, ...] = ()
    entry_trigger_rules: tuple[str, ...] = ()
    exit_rules: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
