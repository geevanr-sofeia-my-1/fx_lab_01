"""Dukascopy mapping helpers."""

from __future__ import annotations

from fxlab.data.providers.base import UnsupportedInstrumentError, UnsupportedTimeframeError
from fxlab.domain.enums import Pair, Timeframe

DUKASCOPY_PAIR_MAP: dict[Pair, str] = {
    Pair.EURUSD: "EURUSD",
    Pair.GBPUSD: "GBPUSD",
    Pair.USDJPY: "USDJPY",
    Pair.AUDUSD: "AUDUSD",
    Pair.USDCAD: "USDCAD",
    Pair.USDCHF: "USDCHF",
}

DUKASCOPY_TIMEFRAME_MAP: dict[Timeframe, str] = {
    Timeframe.M15: "15m",
    Timeframe.H1: "1h",
    Timeframe.H4: "4h",
    Timeframe.D1: "1d",
}


def map_pair_to_dukascopy(pair: Pair) -> str:
    """Map a canonical pair to the Dukascopy instrument identifier."""
    try:
        return DUKASCOPY_PAIR_MAP[pair]
    except KeyError as exc:
        raise UnsupportedInstrumentError(f"Unsupported Dukascopy pair mapping: {pair}") from exc


def map_timeframe_to_dukascopy(timeframe: Timeframe) -> str:
    """Map a canonical timeframe to the Dukascopy interval identifier."""
    try:
        return DUKASCOPY_TIMEFRAME_MAP[timeframe]
    except KeyError as exc:
        raise UnsupportedTimeframeError(
            f"Unsupported Dukascopy timeframe mapping: {timeframe}"
        ) from exc
