"""Stable project-wide constants."""

from pathlib import Path

PROJECT_NAME = "fxlab"
DEFAULT_TIMEZONE = "UTC"
ARTIFACT_SUBDIRECTORIES = (
    "raw",
    "canonical",
    "features",
    "runs",
    "reports",
    "logs",
    "registry",
    "cache",
)
CONFIG_SUBDIRECTORIES = (
    "app",
    "datasets",
    "features",
    "strategies",
    "execution",
    "risk",
    "experiments",
    "validation",
    "reports",
)
TEST_SUBDIRECTORIES = ("unit", "integration", "regression", "fixtures")
SRC_ROOT_NAME = Path("src")
