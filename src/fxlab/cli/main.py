"""Main CLI entry point."""

from __future__ import annotations

import argparse
from pathlib import Path

from fxlab.config.app import AppConfig
from fxlab.config.loader import load_yaml_config
from fxlab.logging import configure_logging, get_logger
from fxlab.paths import ensure_project_structure


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level argument parser."""
    parser = argparse.ArgumentParser(description="FXLab bootstrap CLI")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/app/bootstrap.yaml"),
        help="Path to an application config file.",
    )
    return parser


def main() -> None:
    """Run the bootstrap CLI."""
    args = build_parser().parse_args()
    ensure_project_structure()
    app_config = load_yaml_config(args.config, AppConfig)
    configure_logging(app_config.logging)
    logger = get_logger(__name__)
    logger.info("FXLab bootstrap complete for environment=%s", app_config.environment)
    print(f"fxlab bootstrap ready [{app_config.environment}]")
