"""Logging bootstrap tests."""

import logging

from fxlab.logging import LoggingConfig, configure_logging, get_logger


def test_configure_logging_and_get_logger() -> None:
    configure_logging(LoggingConfig(level="DEBUG"))
    logger = get_logger("fxlab.tests")

    assert logger.name == "fxlab.tests"
    assert logging.getLogger().getEffectiveLevel() == logging.DEBUG
