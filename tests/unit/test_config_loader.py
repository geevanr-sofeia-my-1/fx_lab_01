"""Configuration loader smoke tests."""

from pathlib import Path

import pytest

from fxlab.config import AppConfig, load_yaml_config
from fxlab.exceptions import ConfigError


def test_load_yaml_config_roundtrip() -> None:
    config = load_yaml_config(Path("configs/app/bootstrap.yaml"), AppConfig)
    assert config.environment == "development"
    assert config.logging.level == "INFO"


def test_missing_config_raises_config_error() -> None:
    with pytest.raises(ConfigError):
        load_yaml_config(Path("configs/app/missing.yaml"), AppConfig)
