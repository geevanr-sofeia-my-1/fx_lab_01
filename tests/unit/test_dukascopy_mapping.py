"""Dukascopy mapping tests."""

from fxlab.data.providers.base import UnsupportedInstrumentError, UnsupportedTimeframeError
from fxlab.data.providers.mapping import (
    DUKASCOPY_PAIR_MAP,
    map_pair_to_dukascopy,
    map_timeframe_to_dukascopy,
)


def test_all_initial_pairs_have_explicit_dukascopy_mappings() -> None:
    assert len(DUKASCOPY_PAIR_MAP) == 6
    assert map_pair_to_dukascopy("EURUSD") == "EURUSD"
    assert map_pair_to_dukascopy("USDCHF") == "USDCHF"


def test_supported_timeframes_map_deterministically() -> None:
    assert map_timeframe_to_dukascopy("15m") == "15m"
    assert map_timeframe_to_dukascopy("1H") == "1h"
    assert map_timeframe_to_dukascopy("4H") == "4h"
    assert map_timeframe_to_dukascopy("1D") == "1d"


def test_invalid_pair_mapping_fails_clearly() -> None:
    try:
        map_pair_to_dukascopy("XAUUSD")  # type: ignore[arg-type]
    except UnsupportedInstrumentError:
        pass
    else:
        raise AssertionError("Expected unsupported instrument mapping to fail")


def test_invalid_timeframe_mapping_fails_clearly() -> None:
    try:
        map_timeframe_to_dukascopy("5m")  # type: ignore[arg-type]
    except UnsupportedTimeframeError:
        pass
    else:
        raise AssertionError("Expected unsupported timeframe mapping to fail")
