"""Deterministic hashing helpers."""

from __future__ import annotations

import hashlib
from pathlib import Path


def sha256_bytes(payload: bytes) -> str:
    """Return a stable SHA-256 digest for raw bytes."""
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    """Return a stable SHA-256 digest for a file."""
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()
