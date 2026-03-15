"""SQLite registry initialization."""
# ruff: noqa: I001

from __future__ import annotations

import sqlite3  # noqa: I001
from pathlib import Path


SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    run_id TEXT PRIMARY KEY,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    dataset_fingerprint TEXT NOT NULL,
    strategy_config_hash TEXT NOT NULL,
    validation_plan_id TEXT NOT NULL,
    random_seed INTEGER NOT NULL,
    code_version TEXT,
    artifact_path TEXT,
    error_message TEXT
);
CREATE INDEX IF NOT EXISTS idx_runs_dedupe
ON runs(dataset_fingerprint, strategy_config_hash, validation_plan_id, random_seed);
"""


def initialize_registry(db_path: Path) -> sqlite3.Connection:
    """Initialize the registry database and return a connection."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.executescript(SCHEMA)
    connection.commit()
    return connection
