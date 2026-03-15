"""Repository path helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from fxlab.constants import ARTIFACT_SUBDIRECTORIES, CONFIG_SUBDIRECTORIES, TEST_SUBDIRECTORIES


@dataclass(frozen=True)
class ProjectPaths:
    """Resolved repository paths."""

    repo_root: Path
    src_root: Path
    package_root: Path
    config_root: Path
    artifacts_root: Path
    docs_root: Path
    scripts_root: Path
    tests_root: Path


def discover_repo_root(start: Path | None = None) -> Path:
    """Find the repository root by walking upward to `pyproject.toml`."""
    current = (start or Path(__file__)).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").exists():
            return candidate
    raise FileNotFoundError("Could not locate repository root from current path.")


def get_project_paths(repo_root: Path | None = None) -> ProjectPaths:
    """Return canonical repository path locations."""
    root = (repo_root or discover_repo_root()).resolve()
    return ProjectPaths(
        repo_root=root,
        src_root=root / "src",
        package_root=root / "src" / "fxlab",
        config_root=root / "configs",
        artifacts_root=root / "artifacts",
        docs_root=root / "docs",
        scripts_root=root / "scripts",
        tests_root=root / "tests",
    )


def ensure_project_structure(repo_root: Path | None = None) -> ProjectPaths:
    """Create the baseline repository directory structure if it does not already exist."""
    paths = get_project_paths(repo_root)
    required_directories = [
        paths.src_root,
        paths.package_root,
        paths.config_root,
        paths.artifacts_root,
        paths.docs_root,
        paths.scripts_root,
        paths.tests_root,
    ]
    required_directories.extend(paths.config_root / name for name in CONFIG_SUBDIRECTORIES)
    required_directories.extend(paths.artifacts_root / name for name in ARTIFACT_SUBDIRECTORIES)
    required_directories.extend(paths.tests_root / name for name in TEST_SUBDIRECTORIES)

    for directory in required_directories:
        directory.mkdir(parents=True, exist_ok=True)
    return paths
