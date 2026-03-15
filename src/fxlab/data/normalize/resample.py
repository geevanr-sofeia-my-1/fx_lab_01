"""Deterministic canonical resampling."""

from __future__ import annotations

from collections.abc import Sequence

from fxlab.domain.bars import CanonicalBar
from fxlab.domain.enums import Timeframe

TIMEFRAME_SECONDS: dict[Timeframe, int] = {
    Timeframe.M15: 15 * 60,
    Timeframe.H1: 60 * 60,
    Timeframe.H4: 4 * 60 * 60,
    Timeframe.D1: 24 * 60 * 60,
}


def resample_bars(
    bars: Sequence[CanonicalBar],
    *,
    target_timeframe: Timeframe,
) -> tuple[CanonicalBar, ...]:
    """Resample canonical bars into a higher timeframe deterministically."""
    if not bars:
        return ()

    source_seconds = TIMEFRAME_SECONDS[bars[0].timeframe]
    target_seconds = TIMEFRAME_SECONDS[target_timeframe]
    if target_seconds <= source_seconds:
        raise ValueError("target timeframe must be higher than source timeframe")
    if target_seconds % source_seconds != 0:
        raise ValueError("target timeframe must be an integer multiple of source timeframe")

    ratio = target_seconds // source_seconds
    aggregated: list[CanonicalBar] = []
    for index in range(0, len(bars), ratio):
        chunk = list(bars[index : index + ratio])
        if len(chunk) < ratio:
            break

        first = chunk[0]
        last = chunk[-1]
        aggregated.append(
            CanonicalBar(
                pair=first.pair,
                timeframe=target_timeframe,
                timestamp=first.timestamp,
                open=first.open,
                high=max(bar.high for bar in chunk),
                low=min(bar.low for bar in chunk),
                close=last.close,
                volume=sum(bar.volume or 0.0 for bar in chunk),
                tick_volume=sum(bar.tick_volume or 0.0 for bar in chunk),
                spread=chunk[-1].spread,
                source=first.source,
                provider=first.provider,
                source_instrument=first.source_instrument,
                price_basis=first.price_basis,
                is_complete_bar=all(bar.is_complete_bar for bar in chunk),
                session_asia=any(bar.session_asia for bar in chunk),
                session_london=any(bar.session_london for bar in chunk),
                session_newyork=any(bar.session_newyork for bar in chunk),
            )
        )
    return tuple(aggregated)
