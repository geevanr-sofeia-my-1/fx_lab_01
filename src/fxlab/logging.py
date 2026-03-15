"""Logging configuration helpers."""

from __future__ import annotations

import logging
from dataclasses import dataclass


@dataclass(frozen=True)
class LoggingConfig:
    """Minimal logging configuration."""

    level: str = "INFO"
    format: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def configure_logging(config: LoggingConfig | None = None) -> None:
    """Configure application logging in a deterministic way."""
    resolved = config or LoggingConfig()
    logging.basicConfig(level=resolved.level, format=resolved.format, force=True)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger."""
    return logging.getLogger(name)
