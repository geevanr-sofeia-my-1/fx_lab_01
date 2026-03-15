"""Enumerations shared across the lab."""

from __future__ import annotations

from enum import StrEnum


class Timeframe(StrEnum):
    """Supported canonical timeframes."""

    M15 = "15m"
    H1 = "1H"
    H4 = "4H"
    D1 = "1D"


class Pair(StrEnum):
    """Initial FX universe."""

    EURUSD = "EURUSD"
    GBPUSD = "GBPUSD"
    USDJPY = "USDJPY"
    AUDUSD = "AUDUSD"
    USDCAD = "USDCAD"
    USDCHF = "USDCHF"


class PriceBasis(StrEnum):
    """Canonical price basis declaration."""

    BID = "bid"
    ASK = "ask"
    MID = "mid"
    PROVIDER_DEFAULT = "provider_default"


class EntryTiming(StrEnum):
    """Supported entry timing assumptions."""

    NEXT_BAR_OPEN = "next_bar_open"


class PositionMode(StrEnum):
    """Supported position accounting modes."""

    NETTING = "netting"
    NON_NETTING = "non_netting"
