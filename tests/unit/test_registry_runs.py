"""Run registry tests."""

import shutil
import uuid
from datetime import UTC, datetime
from pathlib import Path

from fxlab.domain.manifests import RunMetadata
from fxlab.registry.db import initialize_registry
from fxlab.registry.runs import create_run, find_duplicate_run, update_run_status


def _metadata(run_id: str) -> RunMetadata:
    return RunMetadata(
        run_id=run_id,
        timestamp=datetime(2024, 1, 1, tzinfo=UTC),
        dataset_fingerprint="dataset-abc",
        strategy_config_hash="strategy-xyz",
        validation_plan_id="standard",
        random_seed=7,
        code_version="0.1.0",
    )


def test_create_and_update_run() -> None:
    scratch = Path("artifacts") / "cache" / f"test_registry_{uuid.uuid4().hex}"
    scratch.mkdir(parents=True, exist_ok=True)
    try:
        connection = initialize_registry(scratch / "registry.sqlite")
        record = create_run(connection, _metadata("run-1"))
        assert record.status == "created"

        updated = update_run_status(
            connection,
            "run-1",
            status="completed",
            artifact_path="artifacts/runs/run-1",
        )
        assert updated.status == "completed"
        assert updated.artifact_path == "artifacts/runs/run-1"
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def test_find_duplicate_run_detects_matching_identity() -> None:
    scratch = Path("artifacts") / "cache" / f"test_registry_{uuid.uuid4().hex}"
    scratch.mkdir(parents=True, exist_ok=True)
    try:
        connection = initialize_registry(scratch / "registry.sqlite")
        create_run(connection, _metadata("run-1"))

        duplicate = find_duplicate_run(
            connection,
            dataset_fingerprint="dataset-abc",
            strategy_config_hash="strategy-xyz",
            validation_plan_id="standard",
            random_seed=7,
        )
        assert duplicate is not None
        assert duplicate.run_id == "run-1"
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def test_failed_run_persists_error_message() -> None:
    scratch = Path("artifacts") / "cache" / f"test_registry_{uuid.uuid4().hex}"
    scratch.mkdir(parents=True, exist_ok=True)
    try:
        connection = initialize_registry(scratch / "registry.sqlite")
        create_run(connection, _metadata("run-1"))
        failed = update_run_status(
            connection,
            "run-1",
            status="failed",
            error_message="provider timeout",
        )
        assert failed.status == "failed"
        assert failed.error_message == "provider timeout"
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
