"""Configuration loading utilities."""

from __future__ import annotations

from pathlib import Path
from typing import TypeVar

import yaml
from pydantic import ValidationError

from fxlab.exceptions import ConfigError

T = TypeVar("T")


def load_yaml_config(path: Path, model_type: type[T]) -> T:
    """Load YAML into a typed config model."""
    try:
        with path.open("r", encoding="utf-8") as handle:
            raw = yaml.safe_load(handle) or {}
    except FileNotFoundError as exc:
        raise ConfigError(f"Config file not found: {path}") from exc

    try:
        return model_type.model_validate(raw)
    except ValidationError as exc:
        raise ConfigError(f"Invalid config at {path}: {exc}") from exc
