"""Raw download storage path helpers."""

from __future__ import annotations

from pathlib import Path

from fxlab.domain.enums import Pair, Timeframe
from fxlab.paths import get_project_paths


def raw_download_directory(
    pair: Pair,
    timeframe: Timeframe,
    download_job_id: str,
    repo_root: Path | None = None,
) -> Path:
    """Return the immutable raw download directory for a job."""
    paths = get_project_paths(repo_root)
    return paths.artifacts_root / "raw" / "dukascopy" / pair / timeframe / download_job_id
