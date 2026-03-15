"""Dataset fingerprinting and quality summaries."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from fxlab.domain.bars import CanonicalBar
from fxlab.domain.manifests import DatasetFingerprint
from fxlab.utils.hashing import sha256_bytes


@dataclass(frozen=True)
class DatasetQualitySummary:
    """Compact quality summary for a canonical dataset."""

    row_count: int
    start: str
    end: str
    duplicate_count: int
    null_volume_count: int
    null_tick_volume_count: int
    null_spread_count: int


def build_dataset_fingerprint(
    bars: Sequence[CanonicalBar],
    *,
    preprocessing_version: str,
) -> DatasetFingerprint:
    """Build a deterministic dataset fingerprint from canonical bars."""
    if not bars:
        raise ValueError("cannot fingerprint an empty dataset")

    serialized = "\n".join(
        "|".join(
            [
                bar.pair,
                bar.timeframe,
                bar.timestamp.isoformat(),
                f"{bar.open:.10f}",
                f"{bar.high:.10f}",
                f"{bar.low:.10f}",
                f"{bar.close:.10f}",
                f"{(bar.volume or 0.0):.10f}",
                f"{(bar.tick_volume or 0.0):.10f}",
                f"{(bar.spread or 0.0):.10f}",
                bar.provider,
                bar.price_basis,
            ]
        )
        for bar in bars
    ).encode("utf-8")
    digest = sha256_bytes(serialized)
    first = bars[0]
    last = bars[-1]
    return DatasetFingerprint(
        fingerprint=digest,
        pair=first.pair,
        timeframe=first.timeframe,
        provider=first.provider,
        price_basis=first.price_basis,
        start=first.timestamp,
        end=last.timestamp,
        row_count=len(bars),
        preprocessing_version=preprocessing_version,
    )


def summarize_dataset_quality(bars: Sequence[CanonicalBar]) -> DatasetQualitySummary:
    """Summarize a canonical dataset for audit-friendly validation output."""
    if not bars:
        raise ValueError("cannot summarize an empty dataset")
    timestamps = [bar.timestamp for bar in bars]
    duplicate_count = len(timestamps) - len(set(timestamps))
    return DatasetQualitySummary(
        row_count=len(bars),
        start=bars[0].timestamp.isoformat(),
        end=bars[-1].timestamp.isoformat(),
        duplicate_count=duplicate_count,
        null_volume_count=sum(bar.volume is None for bar in bars),
        null_tick_volume_count=sum(bar.tick_volume is None for bar in bars),
        null_spread_count=sum(bar.spread is None for bar in bars),
    )
