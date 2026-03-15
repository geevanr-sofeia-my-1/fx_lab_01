"""Project path utility tests."""

import shutil
import uuid
from pathlib import Path

from fxlab.paths import ensure_project_structure


def test_ensure_project_structure_creates_expected_directories() -> None:
    repo_root = Path("artifacts") / "cache" / f"test_repo_{uuid.uuid4().hex}"
    repo_root.mkdir(parents=True, exist_ok=True)
    try:
        (repo_root / "pyproject.toml").write_text(
            "[project]\nname='fxlab'\nversion='0.1.0'\n",
            encoding="utf-8",
        )

        paths = ensure_project_structure(repo_root)

        assert paths.package_root.exists()
        assert (repo_root / "tests" / "unit").exists()
        assert (repo_root / "artifacts" / "logs").exists()
        assert (repo_root / "configs" / "app").exists()
    finally:
        shutil.rmtree(repo_root, ignore_errors=True)
