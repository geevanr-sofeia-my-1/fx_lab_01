"""Execution configuration models."""

from __future__ import annotations

from pydantic import Field

from fxlab.config.schema_base import FXLabBaseModel
from fxlab.domain.enums import EntryTiming, PositionMode


class ExecutionConfig(FXLabBaseModel):
    """Execution assumptions."""

    schema_version: str = "1"
    entry_timing: EntryTiming = EntryTiming.NEXT_BAR_OPEN
    position_mode: PositionMode = PositionMode.NETTING
    spread_pips: float = Field(ge=0.0, default=1.2)
    slippage_pips: float = Field(ge=0.0, default=0.2)
    pessimistic_same_bar_exit: bool = True
