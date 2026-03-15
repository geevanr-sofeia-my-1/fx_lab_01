"""Raw download manifest tests."""

import json
import shutil
import uuid
from datetime import UTC, datetime
from pathlib import Path

from fxlab.data.download.manifests import (
    build_raw_download_manifest,
    write_raw_download_manifest,
)
from fxlab.data.download.storage import raw_download_directory
from fxlab.data.providers.base import ProviderDownloadResult, ProviderRequest


def _make_scratch_dir() -> Path:
    scratch = Path("artifacts") / "cache" / f"test_raw_manifest_{uuid.uuid4().hex}"
    scratch.mkdir(parents=True, exist_ok=True)
    return scratch


def test_build_raw_download_manifest_computes_artifact_hashes() -> None:
    scratch = _make_scratch_dir()
    try:
        artifact = scratch / "chunk.csv"
        artifact.write_text("timestamp,open\n2024-01-01T00:00:00Z,1.1000\n", encoding="utf-8")
        request = ProviderRequest(
            pair="EURUSD",
            timeframe="1H",
            start=datetime(2024, 1, 1, tzinfo=UTC),
            end=datetime(2024, 2, 1, tzinfo=UTC),
            price_basis="mid",
        )
        result = ProviderDownloadResult(
            provider_name="dukascopy",
            raw_artifact_paths=(artifact,),
            request=request,
            retrieved_at=datetime(2024, 2, 2, tzinfo=UTC),
            provider_payload_format="csv",
            source_instrument="EURUSD",
            provider_timeframe="1h",
        )

        manifest = build_raw_download_manifest(
            result,
            package_version="0.1.0",
            preprocessing_version="1",
        )

        assert manifest.provider_name == "dukascopy"
        assert manifest.artifacts[0].path == artifact
        assert len(manifest.artifacts[0].sha256) == 64
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def test_write_raw_download_manifest_is_json_serializable() -> None:
    scratch = _make_scratch_dir()
    try:
        artifact = scratch / "chunk.csv"
        artifact.write_text("x", encoding="utf-8")
        request = ProviderRequest(
            pair="EURUSD",
            timeframe="1H",
            start=datetime(2024, 1, 1, tzinfo=UTC),
            end=datetime(2024, 2, 1, tzinfo=UTC),
            price_basis="mid",
        )
        result = ProviderDownloadResult(
            provider_name="dukascopy",
            raw_artifact_paths=(artifact,),
            request=request,
            retrieved_at=datetime(2024, 2, 2, tzinfo=UTC),
            provider_payload_format="csv",
            source_instrument="EURUSD",
            provider_timeframe="1h",
        )
        manifest = build_raw_download_manifest(
            result,
            package_version="0.1.0",
            preprocessing_version="1",
        )

        destination = scratch / "manifest.json"
        write_raw_download_manifest(manifest, destination)

        payload = json.loads(destination.read_text(encoding="utf-8"))
        assert payload["provider_name"] == "dukascopy"
        assert payload["artifacts"][0]["path"].endswith("chunk.csv")
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def test_raw_download_directory_uses_expected_layout() -> None:
    scratch = _make_scratch_dir()
    try:
        download_path = raw_download_directory("EURUSD", "1H", "job-123", repo_root=scratch)
        assert (
            download_path
            == scratch.resolve()
            / "artifacts"
            / "raw"
            / "dukascopy"
            / "EURUSD"
            / "1H"
            / "job-123"
        )
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
