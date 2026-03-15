"""Manifest and reproducibility schema tests."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from fxlab.domain.manifests import DatasetFingerprint, RunMetadata


def test_dataset_fingerprint_validates() -> None:
    fingerprint = DatasetFingerprint(
        fingerprint="abc123",
        pair="EURUSD",
        timeframe="1H",
        provider="dukascopy",
        price_basis="mid",
        start=datetime(2024, 1, 1, tzinfo=UTC),
        end=datetime(2024, 2, 1, tzinfo=UTC),
        row_count=100,
        preprocessing_version="1",
    )
    assert fingerprint.row_count == 100


def test_run_metadata_rejects_naive_timestamp() -> None:
    with pytest.raises(ValidationError):
        RunMetadata(
            run_id="run-1",
            timestamp=datetime(2024, 1, 1),
            dataset_fingerprint="abc123",
            strategy_config_hash="cfg123",
            validation_plan_id="standard",
            random_seed=7,
        )
