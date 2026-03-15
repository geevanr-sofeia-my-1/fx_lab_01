"""Run registry operations."""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime

from fxlab.domain.manifests import RunMetadata
from fxlab.registry.models import RunRecord


def create_run(
    connection: sqlite3.Connection,
    metadata: RunMetadata,
    *,
    status: str = "created",
    artifact_path: str | None = None,
) -> RunRecord:
    """Insert a new run record."""
    timestamp = datetime.now(tz=UTC).isoformat()
    connection.execute(
        """
        INSERT INTO runs (
            run_id, status, created_at, updated_at,
            dataset_fingerprint, strategy_config_hash,
            validation_plan_id, random_seed, code_version,
            artifact_path, error_message
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            metadata.run_id,
            status,
            timestamp,
            timestamp,
            metadata.dataset_fingerprint,
            metadata.strategy_config_hash,
            metadata.validation_plan_id,
            metadata.random_seed,
            metadata.code_version,
            artifact_path,
            None,
        ),
    )
    connection.commit()
    return get_run(connection, metadata.run_id)


def update_run_status(
    connection: sqlite3.Connection,
    run_id: str,
    *,
    status: str,
    artifact_path: str | None = None,
    error_message: str | None = None,
) -> RunRecord:
    """Update run status and optional artifact/error fields."""
    timestamp = datetime.now(tz=UTC).isoformat()
    connection.execute(
        """
        UPDATE runs
        SET status = ?, updated_at = ?, artifact_path = COALESCE(?, artifact_path),
            error_message = ?
        WHERE run_id = ?
        """,
        (status, timestamp, artifact_path, error_message, run_id),
    )
    connection.commit()
    return get_run(connection, run_id)


def find_duplicate_run(
    connection: sqlite3.Connection,
    *,
    dataset_fingerprint: str,
    strategy_config_hash: str,
    validation_plan_id: str,
    random_seed: int,
) -> RunRecord | None:
    """Find an existing run with the same reproducibility identity."""
    cursor = connection.execute(
        """
        SELECT run_id, status, created_at, updated_at,
               dataset_fingerprint, strategy_config_hash,
               validation_plan_id, random_seed, code_version,
               artifact_path, error_message
        FROM runs
        WHERE dataset_fingerprint = ?
          AND strategy_config_hash = ?
          AND validation_plan_id = ?
          AND random_seed = ?
        ORDER BY created_at ASC
        LIMIT 1
        """,
        (dataset_fingerprint, strategy_config_hash, validation_plan_id, random_seed),
    )
    row = cursor.fetchone()
    return _row_to_record(row) if row is not None else None


def get_run(connection: sqlite3.Connection, run_id: str) -> RunRecord:
    """Load one run by id."""
    cursor = connection.execute(
        """
        SELECT run_id, status, created_at, updated_at,
               dataset_fingerprint, strategy_config_hash,
               validation_plan_id, random_seed, code_version,
               artifact_path, error_message
        FROM runs
        WHERE run_id = ?
        """,
        (run_id,),
    )
    row = cursor.fetchone()
    if row is None:
        raise KeyError(f"unknown run_id: {run_id}")
    return _row_to_record(row)


def _row_to_record(row: tuple[object, ...]) -> RunRecord:
    return RunRecord(
        run_id=str(row[0]),
        status=str(row[1]),
        created_at=str(row[2]),
        updated_at=str(row[3]),
        dataset_fingerprint=str(row[4]),
        strategy_config_hash=str(row[5]),
        validation_plan_id=str(row[6]),
        random_seed=int(row[7]),
        code_version=None if row[8] is None else str(row[8]),
        artifact_path=None if row[9] is None else str(row[9]),
        error_message=None if row[10] is None else str(row[10]),
    )
