"""Registry persistence models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RunRecord:
    """Persisted run metadata."""

    run_id: str
    status: str
    created_at: str
    updated_at: str
    dataset_fingerprint: str
    strategy_config_hash: str
    validation_plan_id: str
    random_seed: int
    code_version: str | None
    artifact_path: str | None
    error_message: str | None
