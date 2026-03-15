# REPO_STRUCTURE.md

## Purpose

This document defines the intended repository structure for the FX systematic strategy lab.

It exists to remove ambiguity for coding agents and human developers about:

- module placement
- responsibility boundaries
- artifact locations
- config layout
- test layout
- naming conventions

Follow this structure unless a later architecture revision explicitly changes it.

---

## Top-level repository layout

```text
fx-systematic-lab/
├── AGENTS.md
├── PLANS.md
├── TASKS.md
├── TASKS_EXECUTION_ORDER.md
├── REPO_STRUCTURE.md
├── README.md
├── pyproject.toml
├── Makefile
├── .gitignore
├── configs/
├── docs/
├── artifacts/
├── scripts/
├── src/
│   └── fxlab/
└── tests/



Top-level directory responsibilities
configs/

Holds all user-editable configuration files.

Use this for:

dataset download jobs

feature jobs

strategy definitions

execution settings

risk settings

experiment runs

validation plans

report generation jobs

Configs must be declarative and versionable.

docs/

Holds human-oriented documentation.

Use this for:

architecture notes

execution assumptions

reproducibility notes

strategy DSL guide

data contracts

troubleshooting

onboarding notes

Do not put live run artifacts here.

artifacts/

Holds generated outputs.

Use this for:

raw downloads

normalized datasets

feature tables

manifests

run outputs

metrics

reports

logs

registry databases

cached intermediates where appropriate

Artifacts must never be treated as source code.

scripts/

Holds thin command wrappers and utility scripts.

Use this for:

bootstrapping commands

local admin scripts

migration helpers

artifact cleanup tools

reproducibility helpers

Business logic should stay in src/fxlab/, not in scripts.

src/fxlab/

Holds all production code.

This is the main application package.

tests/

Holds all tests.

Split by test purpose:

unit

integration

regression

fixtures

Source package structure
src/fxlab/
├── __init__.py
├── version.py
├── logging.py
├── paths.py
├── constants.py
├── exceptions.py
├── cli/
├── config/
├── domain/
├── data/
├── features/
├── strategy/
├── execution/
├── portfolio/
├── metrics/
├── experiments/
├── validation/
├── registry/
├── reporting/
└── utils/
Source module responsibilities
src/fxlab/version.py

Defines package version exposure.

src/fxlab/logging.py

Defines logging configuration and logger creation helpers.

src/fxlab/paths.py

Defines path resolution logic for:

repo root

config root

artifact root

default subdirectories

src/fxlab/constants.py

Defines stable project-wide constants.

Examples:

supported initial FX pairs

default time zone rules

canonical column names

default artifact subdirectory names

src/fxlab/exceptions.py

Defines project-specific exceptions.

CLI package
src/fxlab/cli/
├── __init__.py
├── main.py
├── download.py
├── normalize.py
├── features.py
├── backtest.py
├── sweep.py
├── validate.py
└── report.py
Responsibility

Expose command-line entry points only.

CLI modules must:

parse arguments

load configs

call service-layer code

return clear exit codes

CLI modules must not contain core business logic.

Config package
src/fxlab/config/
├── __init__.py
├── loader.py
├── schema_base.py
├── dataset.py
├── feature_job.py
├── strategy.py
├── execution.py
├── risk.py
├── experiment.py
├── validation.py
└── report.py
Responsibility

Own configuration parsing, validation, defaults, and schema version handling.

Rules:

configs must fail loudly when invalid

schema objects must be serializable

hidden defaults are not allowed unless explicitly documented

Domain package
src/fxlab/domain/
├── __init__.py
├── enums.py
├── identifiers.py
├── bars.py
├── signals.py
├── orders.py
├── trades.py
├── positions.py
├── account.py
└── manifests.py
Responsibility

Own core typed value objects and domain entities.

This package should contain the shared language of the system.

Examples:

timeframe enum

pair enum

price basis enum

canonical bar record

order model

trade model

account state model

dataset manifest model

Keep this package clean and stable.

Data package
src/fxlab/data/
├── __init__.py
├── providers/
│   ├── __init__.py
│   ├── base.py
│   ├── dukascopy.py
│   └── mapping.py
├── download/
│   ├── __init__.py
│   ├── jobs.py
│   ├── manifests.py
│   └── storage.py
├── normalize/
│   ├── __init__.py
│   ├── canonical.py
│   ├── validate.py
│   ├── resample.py
│   └── quality.py
└── sessions/
    ├── __init__.py
    └── labels.py
Responsibility

Own the full historical data pipeline.

providers/

Contains provider abstractions and implementations.

Rules:

all vendor-specific logic stays here

v1 historical source of truth is Dukascopy through dukascopy-python

downstream modules must not call vendor libraries directly

download/

Contains raw download orchestration and metadata capture.

normalize/

Contains raw-to-canonical conversion logic.

sessions/

Contains deterministic session labeling logic.

Features package
src/fxlab/features/
├── __init__.py
├── base.py
├── registry.py
├── runner.py
├── alignment.py
├── naming.py
├── trend.py
├── momentum.py
├── volatility.py
├── channels.py
├── regime.py
└── candlestick/
    ├── __init__.py
    ├── base.py
    ├── common.py
    └── thresholds.py
Responsibility

Own feature computation.

Rules:

features must be reproducible

alignment must be explicit

no future leakage

output column naming must be stable

feature jobs must record parameters and fingerprints

Suggested module use:

trend.py: SMA, EMA, slopes, structure helpers

momentum.py: RSI, MACD, stochastic

volatility.py: ATR, rolling volatility

channels.py: Bollinger, Donchian

regime.py: compression, expansion, session-derived features

Strategy package
src/fxlab/strategy/
├── __init__.py
├── schema.py
├── compiler.py
├── primitives.py
├── composition.py
├── filters.py
├── exits.py
├── sizing_bridge.py
└── templates/
    ├── __init__.py
    └── baseline.py
Responsibility

Own strategy definition and signal generation.

Rules:

strategies must be declarative

strategy logic must be composable

primitives and composition must be tested independently

strategy code must not directly manage account state

schema.py

Strategy DSL schema.

compiler.py

Converts config-defined strategies into executable signal graphs or rule objects.

primitives.py

Crosses, thresholds, touches, breakouts.

composition.py

AND, OR, NOT, optional sequential logic.

filters.py

Regime filters, session filters, trend filters.

exits.py

Exit rule builders, not fill logic.

sizing_bridge.py

Connects strategy-defined sizing intent to the risk engine.

Execution package
src/fxlab/execution/
├── __init__.py
├── engine.py
├── fills.py
├── costs.py
├── stops.py
├── targets.py
├── tie_break.py
└── events.py
Responsibility

Translate signals into fills under explicit assumptions.

Rules:

next-bar-open should be the default conservative entry model

same-bar fantasy fills must not be assumed

stop/target tie-break logic must be explicit

price basis and spread interaction must be visible and testable

Suggested responsibilities:

engine.py: orchestration of order evaluation

fills.py: entry fill rules

costs.py: spread and slippage

stops.py: stop handling

targets.py: target handling

tie_break.py: ambiguous same-bar rule policy

events.py: fill and execution event objects

Portfolio package
src/fxlab/portfolio/
├── __init__.py
├── accounting.py
├── constraints.py
├── equity.py
└── ledger.py
Responsibility

Track account and portfolio state.

Rules:

portfolio state must be deterministic

realized and unrealized PnL must be explicit

constraints must be enforceable independently of strategy generation

Suggested responsibilities:

accounting.py: cash and equity updates

constraints.py: max positions, per-pair cap, exposure limits

equity.py: equity curve generation

ledger.py: trade and event bookkeeping

Metrics package
src/fxlab/metrics/
├── __init__.py
├── trades.py
├── equity.py
├── risk.py
├── grouped.py
└── scoring.py
Responsibility

Compute evaluation metrics.

Rules:

formulas must be documented

metrics must be reproducible from recorded outputs

scoring must not rely on return alone

Suggested responsibilities:

trades.py: win rate, expectancy, profit factor

equity.py: returns, CAGR, drawdowns

risk.py: risk-adjusted metrics

grouped.py: by pair, year, regime, split

scoring.py: composite ranking score

Experiments package
src/fxlab/experiments/
├── __init__.py
├── runner.py
├── single_indicator.py
├── combinations.py
├── artifacts.py
└── reproducibility.py
Responsibility

Run backtest experiments and sweeps.

Rules:

experiments must be config-driven

reproducibility metadata is mandatory

failed runs must be recorded

Suggested responsibilities:

runner.py: generic experiment orchestration

single_indicator.py: single-indicator sweep generation

combinations.py: 2-indicator and 3-indicator controlled search

artifacts.py: run artifact writing

reproducibility.py: config hashes, dataset fingerprints, code version capture

Validation package
src/fxlab/validation/
├── __init__.py
├── splits.py
├── walkforward.py
├── monte_carlo.py
├── sensitivity.py
├── stress.py
└── guards.py
Responsibility

Protect against false discoveries and fragile conclusions.

Rules:

final test segment must stay isolated

validation must be distinct from raw backtest output

robustness checks must be reproducible

Suggested responsibilities:

splits.py: train, validate, test segment logic

walkforward.py: walk-forward execution

monte_carlo.py: deterministic resampling under fixed seed

sensitivity.py: parameter stability tests

stress.py: cost stress and other stress scenarios

guards.py: anti-leakage and anti-selection-bias safeguards

Registry package
src/fxlab/registry/
├── __init__.py
├── db.py
├── models.py
├── runs.py
└── queries.py
Responsibility

Store and query experiment metadata.

Rules:

all runs must be recorded

duplicate runs must be detectable

failed runs must not disappear

Suggested responsibilities:

db.py: DB initialization and connection handling

models.py: persistence models

runs.py: insert and update run records

queries.py: leaderboard and audit queries

Reporting package
src/fxlab/reporting/
├── __init__.py
├── run_summary.py
├── validation_summary.py
├── leaderboard.py
└── warnings.py
Responsibility

Generate readable outputs for humans.

Rules:

reports must point back to run metadata

fragile strategies must be visibly flagged

reports must separate raw performance from validated robustness

Utils package
src/fxlab/utils/
├── __init__.py
├── hashing.py
├── datetime.py
├── io.py
├── pandas_ops.py
└── seeds.py
Responsibility

Small reusable helpers only.

Rules:

do not dump business logic here

keep helpers focused and generic

Artifact structure
artifacts/
├── raw/
│   └── dukascopy/
├── canonical/
├── features/
├── runs/
├── reports/
├── logs/
├── registry/
└── cache/
Artifact directory responsibilities
artifacts/raw/dukascopy/

Stores raw downloaded provider artifacts and raw manifests.

Suggested structure:

artifacts/raw/dukascopy/{pair}/{timeframe}/{download_job_id}/

Contents may include:

raw provider payloads

raw manifest

checksum file

download metadata

Raw artifacts must be immutable after creation.

artifacts/canonical/

Stores normalized datasets.

Suggested structure:

artifacts/canonical/{pair}/{timeframe}/{dataset_fingerprint}/

Contents may include:

canonical parquet files

dataset manifest

quality report

preprocessing version metadata

artifacts/features/

Stores computed feature tables.

Suggested structure:

artifacts/features/{pair}/{timeframe}/{feature_job_fingerprint}/

Contents may include:

feature parquet

feature manifest

feature fingerprint

parameter metadata

artifacts/runs/

Stores run-specific outputs.

Suggested structure:

artifacts/runs/{run_id}/

Contents may include:

resolved config snapshot

dataset fingerprint reference

signal outputs

trade log

equity curve

metrics summary

warnings

validation outputs where relevant

artifacts/reports/

Stores exported human-readable reports.

Suggested structure:

artifacts/reports/{date_or_batch_id}/
artifacts/logs/

Stores pipeline and run logs.

artifacts/registry/

Stores SQLite or DuckDB registry files and backups.

artifacts/cache/

Stores safe-to-rebuild intermediate caches.

Never treat cache as source of truth.

Config structure
configs/
├── datasets/
├── features/
├── strategies/
├── execution/
├── risk/
├── experiments/
├── validation/
└── reports/
Rules

one config concern per file where practical

config names must be descriptive

resolved runtime configs should be copied into run artifacts

Example names:

configs/datasets/eurusd_h1_2022_2024.yaml

configs/features/core_features_h1.yaml

configs/strategies/ema_rsi_atr_baseline.yaml

configs/experiments/single_indicator_sweep_v1.yaml

Test structure
tests/
├── unit/
├── integration/
├── regression/
└── fixtures/
Test directory responsibilities
tests/unit/

Fast isolated tests.

Use for:

enums

schemas

mappings

metric formulas

signal primitives

sizing calculations

tests/integration/

Cross-module tests.

Use for:

provider download flow with mocks

normalization pipeline

feature job execution

backtest vertical slices

registry integration

tests/regression/

Bias and failure-mode protection.

Use for:

lookahead bias traps

same-bar fantasy fill traps

price-basis misuse traps

out-of-sample leakage traps

rerun determinism checks

These tests are mission critical.

tests/fixtures/

Small deterministic datasets and expected outputs.

Use for:

tiny OHLC datasets

ambiguous execution cases

session boundary cases

expected indicator values

expected metrics

manifest samples

Naming conventions
General

use lowercase snake_case for Python modules and functions

use explicit names over short names

avoid vague names like helpers.py, misc.py, stuff.py

Strategy-related

use role-based names:

trend_filter

entry_trigger

exit_rule

sizing_rule

Artifact-related

include stable IDs or fingerprints where reproducibility matters

do not use random filenames without recording them in metadata

Tests

test file names should describe the target:

test_timeframe_enum.py

test_dukascopy_mapping.py

test_rsi_feature_alignment.py

test_same_bar_tie_break_regression.py

Dependency direction rules

Use these rules to avoid architecture drift.

Allowed broad dependency direction

config can be used by orchestration layers

domain should be usable by nearly all layers

data, features, strategy, execution, portfolio, metrics should depend on domain

experiments, validation, reporting, registry, cli may orchestrate lower layers

Avoid

domain depending on higher-level modules

metrics mutating portfolio or execution state

reporting containing business logic

cli containing pipeline logic

vendor library usage outside data/providers/

Initial implementation priority inside repo structure

Build in this order:

config/

domain/

data/providers/

data/download/

data/normalize/

data/sessions/

features/

strategy/

execution/

portfolio/

metrics/

registry/

experiments/

validation/

reporting/

cli/

Reason:

correctness starts with contracts and data

then features and signals

then execution realism

then evaluation and orchestration

then user-facing interfaces

Non-goals for v1 repo structure

Do not add these unless explicitly needed later:

live trading adapters

broker execution connectors

web dashboards

distributed orchestration frameworks

multi-language microservices

plugin systems for untrusted external code

premature high-performance subpackages

Keep v1 tight and trustworthy.

Definition of structure compliance

The repository structure is compliant when:

Every major responsibility has a clear home.

Vendor-specific code exists only under data/providers/.

Artifacts are separated from source code.

Configs are separated from docs and artifacts.

Tests are split by purpose.

Domain objects are stable and reusable.

Reporting is downstream only.

Business logic is not buried inside CLI or scripts.

Reproducibility metadata has a clear storage location.

Anti-bias regression tests have a dedicated home.

Final note

This structure is intentionally conservative.

The lab should first be correct, testable, and reproducible.
Only after that should it become broader, faster, or more complex.


