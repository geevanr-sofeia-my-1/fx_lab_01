"""Raw-to-canonical normalization."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import UTC

from fxlab.data.normalize.validate import validate_sorted_bars, validate_unique_timestamps
from fxlab.data.sessions.labels import label_sessions
from fxlab.domain.bars import CanonicalBar
from fxlab.domain.enums import Pair, PriceBasis, Timeframe


def normalize_raw_bars(
    raw_rows: Iterable[dict[str, object]],
    *,
    pair: Pair,
    timeframe: Timeframe,
    source: str,
    provider: str,
    price_basis: PriceBasis,
    source_instrument: str | None = None,
    drop_duplicates: bool = True,
) -> tuple[CanonicalBar, ...]:
    """Normalize provider-shaped rows into canonical bars.

    Input rows are expected to already contain OHLC-like fields and a timestamp.
    This function intentionally keeps the contract simple for the first slice.
    """
    normalized: list[CanonicalBar] = []
    seen_timestamps = set()

    for row in raw_rows:
        timestamp = row["timestamp"]
        if not hasattr(timestamp, "tzinfo"):
            raise ValueError("raw row timestamp must be datetime-like")
        normalized_timestamp = timestamp.astimezone(UTC)
        derived_sessions = label_sessions(normalized_timestamp)
        bar = CanonicalBar(
            pair=pair,
            timeframe=timeframe,
            timestamp=normalized_timestamp,
            open=float(row["open"]),
            high=float(row["high"]),
            low=float(row["low"]),
            close=float(row["close"]),
            volume=float(row["volume"]) if row.get("volume") is not None else None,
            tick_volume=float(row["tick_volume"]) if row.get("tick_volume") is not None else None,
            spread=float(row["spread"]) if row.get("spread") is not None else None,
            source=source,
            provider=provider,
            source_instrument=source_instrument,
            price_basis=price_basis,
            is_complete_bar=bool(row.get("is_complete_bar", True)),
            session_asia=bool(row.get("session_asia", derived_sessions.asia)),
            session_london=bool(row.get("session_london", derived_sessions.london)),
            session_newyork=bool(row.get("session_newyork", derived_sessions.newyork)),
        )

        if bar.timestamp in seen_timestamps:
            if drop_duplicates:
                continue
            raise ValueError(f"duplicate timestamp encountered: {bar.timestamp.isoformat()}")
        seen_timestamps.add(bar.timestamp)
        normalized.append(bar)

    normalized.sort(key=lambda bar: bar.timestamp)
    validate_sorted_bars(normalized)
    validate_unique_timestamps(normalized)
    return tuple(normalized)
