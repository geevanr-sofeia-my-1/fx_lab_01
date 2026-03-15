"""Application bootstrap configuration models."""

from __future__ import annotations

from fxlab.config.schema_base import FXLabBaseModel
from fxlab.logging import LoggingConfig


class AppConfig(FXLabBaseModel):
    """Top-level bootstrap application configuration."""

    environment: str = "development"
    logging: LoggingConfig = LoggingConfig()
