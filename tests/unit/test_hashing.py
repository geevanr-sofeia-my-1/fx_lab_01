"""Hashing helper tests."""

import shutil
import uuid
from pathlib import Path

from fxlab.utils.hashing import sha256_bytes, sha256_file


def test_sha256_bytes_is_deterministic() -> None:
    payload = b"fxlab"
    assert sha256_bytes(payload) == sha256_bytes(payload)


def test_sha256_file_matches_same_contents() -> None:
    scratch = Path("artifacts") / "cache" / f"test_hashing_{uuid.uuid4().hex}"
    scratch.mkdir(parents=True, exist_ok=True)
    try:
        file_path = scratch / "sample.txt"
        file_path.write_text("fxlab", encoding="utf-8")
        assert sha256_file(file_path) == sha256_bytes(b"fxlab")
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
