"""Configuration package."""

from fxlab.config.app import AppConfig
from fxlab.config.loader import load_yaml_config

__all__ = ["AppConfig", "load_yaml_config"]
