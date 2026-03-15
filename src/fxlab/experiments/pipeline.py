"""End-to-end vertical slice experiment pipeline."""
# ruff: noqa: I001

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from io import StringIO
from pathlib import Path

from fxlab.config.experiment import ExperimentRunConfig
from fxlab.data.download.manifests import build_raw_download_manifest, write_raw_download_manifest
from fxlab.data.normalize.canonical import normalize_raw_bars
from fxlab.data.normalize.quality import build_dataset_fingerprint
from fxlab.data.providers.base import ProviderRequest
from fxlab.data.providers.dukascopy import DukascopyProvider, Fetcher
from fxlab.domain.manifests import RunMetadata
from fxlab.execution.engine import execute_long_only_strategy
from fxlab.experiments.artifacts import RunSummary
from fxlab.features.defaults import build_default_feature_registry
from fxlab.features.runner import run_feature_job
from fxlab.metrics.equity import max_drawdown
from fxlab.metrics.trades import profit_factor
from fxlab.paths import ensure_project_structure
from fxlab.portfolio.accounting import apply_trade_to_account, initialize_account
from fxlab.portfolio.equity import equity_curve_from_account_states
from fxlab.registry.db import initialize_registry
from fxlab.registry.runs import create_run, find_duplicate_run, update_run_status
from fxlab.reporting.run_summary import build_run_summary
from fxlab.risk.sizing import atr_based_size
from fxlab.strategy.compiler import evaluate_strategy
from fxlab.strategy.schema import StrategyDefinition
from fxlab.utils.hashing import sha256_bytes
from fxlab.validation.guards import meets_minimum_trade_count
from fxlab.version import __version__


FEATURE_PATTERN = re.compile(r"^(?P<name>[a-z_]+)_length_(?P<length>\d+)$")


@dataclass(frozen=True)
class VerticalSliceResult:
    """Serializable vertical slice result."""

    run_id: str
    summary: dict[str, object]
    artifact_dir: str


def run_vertical_slice(
    *,
    config: ExperimentRunConfig,
    strategy: StrategyDefinition,
    fetcher: Fetcher,
    repo_root: Path | None = None,
) -> VerticalSliceResult:
    """Run a full mocked vertical slice from provider download to report artifact."""
    paths = ensure_project_structure(repo_root)
    registry_path = paths.artifacts_root / "registry" / "runs.sqlite"
    connection = initialize_registry(registry_path)

    run_identity = sha256_bytes(
        (
            config.model_dump_json()
            + strategy.model_dump_json()
            + __version__
        ).encode("utf-8")
    )[:16]
    run_id = f"run_{run_identity}"
    artifact_dir = paths.artifacts_root / "runs" / run_id
    summary_path = artifact_dir / "run_summary.json"

    duplicate = find_duplicate_run(
        connection,
        dataset_fingerprint=run_identity,
        strategy_config_hash=run_identity,
        validation_plan_id="vertical_slice",
        random_seed=config.random_seed,
    )
    if duplicate is not None and summary_path.exists():
        payload = json.loads(summary_path.read_text(encoding="utf-8"))
        return VerticalSliceResult(
            run_id=run_id,
            summary=payload,
            artifact_dir=str(artifact_dir),
        )

    metadata = RunMetadata(
        run_id=run_id,
        timestamp=datetime.now(tz=UTC),
        dataset_fingerprint=run_identity,
        strategy_config_hash=run_identity,
        validation_plan_id="vertical_slice",
        random_seed=config.random_seed,
        code_version=__version__,
    )
    create_run(connection, metadata, artifact_path=str(artifact_dir))

    request = ProviderRequest(
        pair=config.dataset.pair,
        timeframe=config.dataset.timeframe,
        start=config.dataset.start,
        end=config.dataset.end,
        price_basis=config.dataset.price_basis,
    )
    provider = DukascopyProvider(fetcher=fetcher, repo_root=paths.repo_root)
    download_result = provider.download(request)
    raw_manifest = build_raw_download_manifest(
        download_result,
        package_version=__version__,
        preprocessing_version="1",
    )
    write_raw_download_manifest(raw_manifest, artifact_dir / "raw_manifest.json")

    raw_rows = _read_csv_artifacts(download_result.raw_artifact_paths)
    bars = normalize_raw_bars(
        raw_rows,
        pair=config.dataset.pair,
        timeframe=config.dataset.timeframe,
        source="mocked_dukascopy",
        provider="dukascopy",
        price_basis=config.dataset.price_basis,
        source_instrument=config.dataset.pair,
    )
    dataset_fingerprint = build_dataset_fingerprint(bars, preprocessing_version="1")

    feature_rows = _build_feature_rows(bars, config)
    strategy_rows = evaluate_strategy(strategy, feature_rows)
    execution_rows = _attach_risk_fields(feature_rows, strategy_rows, config)
    trades = execute_long_only_strategy(
        execution_rows,
        spread_pips=config.execution.spread_pips,
        slippage_pips=config.execution.slippage_pips,
    )

    account = initialize_account(config.risk.starting_capital)
    states = [account]
    for trade in trades:
        account = apply_trade_to_account(account, trade)
        states.append(account)
    equity_curve = equity_curve_from_account_states(states)

    net_return = 0.0 if not equity_curve else (equity_curve[-1] - equity_curve[0]) / equity_curve[0]
    summary = RunSummary(
        run_id=run_id,
        candidate_id=strategy.name,
        net_return=net_return,
        max_drawdown=max_drawdown(equity_curve),
        profit_factor=profit_factor(trades),
        trade_count=len(trades),
    )
    summary_payload = build_run_summary(summary)
    summary_payload["dataset_fingerprint"] = dataset_fingerprint.fingerprint
    summary_payload["meets_min_trade_count"] = meets_minimum_trade_count(
        [trade.pnl for trade in trades],
        minimum_trade_count=config.validation.minimum_trade_count,
    )

    artifact_dir.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary_payload, indent=2, sort_keys=True), encoding="utf-8")
    (artifact_dir / "trades.json").write_text(
        json.dumps([trade.model_dump(mode="json") for trade in trades], indent=2, sort_keys=True),
        encoding="utf-8",
    )

    update_run_status(connection, run_id, status="completed", artifact_path=str(artifact_dir))
    return VerticalSliceResult(
        run_id=run_id,
        summary=summary_payload,
        artifact_dir=str(artifact_dir),
    )


def _read_csv_artifacts(paths: tuple[Path, ...]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in paths:
        content = path.read_text(encoding="utf-8")
        reader = csv.DictReader(StringIO(content))
        for row in reader:
            rows.append(
                {
                    "timestamp": datetime.fromisoformat(
                        str(row["timestamp"]).replace("Z", "+00:00")
                    ),
                    "open": float(row["open"]),
                    "high": float(row["high"]),
                    "low": float(row["low"]),
                    "close": float(row["close"]),
                    "volume": float(row["volume"]) if row.get("volume") else None,
                }
            )
    return rows


def _build_feature_rows(
    bars: tuple[object, ...],
    config: ExperimentRunConfig,
) -> tuple[dict[str, object], ...]:
    registry = build_default_feature_registry()
    merged = [
        {
            "timestamp": bar.timestamp.isoformat(),
            "open": bar.open,
            "high": bar.high,
            "low": bar.low,
            "close": bar.close,
        }
        for bar in bars
    ]
    for feature_name in config.strategy.feature_set:
        match = FEATURE_PATTERN.match(feature_name)
        if match is None:
            continue
        result = run_feature_job(
            registry,
            match.group("name"),
            bars,
            length=int(match.group("length")),
        )
        for row, feature_row in zip(merged, result.rows, strict=False):
            for key, value in feature_row.items():
                if key != "timestamp":
                    row[key] = value
    return tuple(merged)


def _attach_risk_fields(
    feature_rows: tuple[dict[str, object], ...],
    strategy_rows: tuple[object, ...],
    config: ExperimentRunConfig,
) -> tuple[dict[str, object], ...]:
    output: list[dict[str, object]] = []
    for row, signal in zip(feature_rows, strategy_rows, strict=False):
        enriched = dict(row)
        enriched["entry_signal"] = signal.entry_signal
        atr_value = row.get("atr_length_3")
        if isinstance(atr_value, (float, int)):
            stop_distance = float(atr_value)
            enriched["stop_loss"] = float(row["close"]) - stop_distance
            enriched["take_profit"] = float(row["close"]) + (stop_distance * 2.0)
            enriched["size"] = atr_based_size(
                equity=config.risk.starting_capital,
                risk_fraction=config.risk.risk_fraction,
                atr_value=stop_distance,
                atr_multiple=1.0,
            )
        else:
            enriched["stop_loss"] = None
            enriched["take_profit"] = None
            enriched["size"] = 1.0
        output.append(enriched)
    return tuple(output)
