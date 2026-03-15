# AGENTS.md

## Mission

Build a research-grade, deterministic, testable foreign exchange systematic strategy lab for idea generation, backtesting, validation, and comparison.

This repository is not a toy backtester. It must prevent false positives caused by lookahead bias, data leakage, incorrect fills, unrealistic cost assumptions, overfitting, or accidental reuse of out-of-sample information.

Read `PLANS.md` before making any non-trivial change.

## Primary Objective

Implement a modular Python system that can:

1. Ingest and normalize historical OHLCV data for major FX pairs, using Dukascopy as the canonical historical source in v1 via `dukascopy-python`.
2. Generate indicator, pattern, regime, and risk features.
3. Define strategies from reusable building blocks instead of ad hoc scripts.
4. Backtest strategies with realistic execution and money management rules.
5. Run systematic experiment sweeps over single indicators, then selected 2-indicator and 3-indicator combinations.
6. Validate candidates using robust out-of-sample procedures.
7. Persist all inputs, outputs, configs, and metrics so results are reproducible.

## Non-Negotiable Rules

1. No lookahead bias:
   - Signals may only use information available at or before decision time.
   - Features that need rolling windows must be shifted appropriately.
   - No same-bar execution based on unseen intrabar extremes unless an explicit intrabar model is implemented and tested.

2. No data leakage:
   - Training, validation, and test segments must remain isolated.
   - Strategy selection must never use the final test segment.
   - Normalization and threshold estimation must respect split boundaries.

3. No silent assumptions:
   - Spread, slippage, position sizing, stop logic, session filters, and fill rules must be explicit in config and logs.
   - Missing values, dropped bars, timezone conversions, and duplicated timestamps must be surfaced.

4. No hidden optimization against the answer:
   - Do not tune on the final out-of-sample results.
   - Do not discard failing trials without recording them.
   - Do not rank strategies by return alone.

5. Reproducibility first:
   - Every experiment must store config, dataset fingerprint, code version, random seed, and result metrics.
   - Re-running the same experiment with the same inputs must produce the same outputs.

6. Correctness before speed:
   - Build the slow, clear, correct path first.
   - Add vectorization or parallelization only after parity tests pass.

7. Source discipline:
   - All historical price downloads in v1 must go through an internal Dukascopy provider adapter built on `dukascopy-python`.
   - Do not scatter direct `dukascopy-python` calls across the codebase.
   - Persist provider metadata with each dataset: provider name, package version, request parameters, instrument mapping, price basis, retrieval timestamp, and raw artifact paths.
   - Raw provider downloads are immutable. Canonical datasets are derived artifacts and must remain reproducible from raw data plus preprocessing version.

## Engineering Standards

- Python 3.11+.
- Use a `src/` layout.
- Prefer pure functions and typed interfaces.
- Add type hints for public functions and dataclasses or pydantic models for configs.
- Keep core logic out of notebooks.
- Keep I/O, feature generation, signal logic, execution, evaluation, and reporting in separate modules.
- Avoid giant scripts. Prefer small modules with narrow responsibilities.
- Use configs, not hard-coded experiment parameters.
- Use UTC internally. Convert broker or source timestamps during ingestion only.
- Historical data acquisition must use `dukascopy-python` behind an internal provider interface.
- Record provider metadata and dataset manifests as first-class artifacts.
- Use Parquet for large tabular datasets and SQLite or DuckDB for experiment metadata and aggregated results.
- Use structured logging.

## Expected Repository Shape

- `src/fxlab/`
  - `data/`: ingestion, validation, normalization, resampling
  - `features/`: indicators, candle patterns, market structure, regimes
  - `signals/`: reusable rule primitives and compositions
  - `execution/`: fills, spread, slippage, order lifecycle
  - `risk/`: sizing, stops, targets, portfolio constraints
  - `backtest/`: engine and portfolio simulation
  - `experiments/`: sweep runner, parameter grids, orchestration
  - `validation/`: walk-forward, Monte Carlo, robustness tests
  - `metrics/`: performance and risk metrics
  - `reporting/`: tables, ranking, artifacts
  - `storage/`: run registry, fingerprints, persistence
  - `config/`: schema and loading
- `tests/`
  - `unit/`
  - `integration/`
  - `regression/`
  - `fixtures/`
- `configs/`
- `docs/`
- `artifacts/` or `outputs/`

Adjust only if there is a strong reason. Keep responsibilities separate.

## Strategy Design Rules

Treat a strategy as a composition of roles:

- Universe: which pair or basket
- Timeframe: bar interval
- Regime filter: when the strategy is allowed to trade
- Setup: state condition, for example trend or compression
- Trigger: exact entry event
- Exit: stop, target, time exit, reversal exit, trailing exit, or combinations
- Sizing: fixed lot, fixed fractional, ATR-based, volatility-targeted, capped fractional
- Portfolio constraints: max open trades, per-pair risk cap, correlation cap

Do not treat a raw indicator as a complete strategy.

For combinations:
- Start with single-indicator strategies under a standardized execution and risk framework.
- Only combine indicators that play distinct roles.
- Avoid redundant combinations where multiple indicators encode the same information.

## Money Management Rules

The lab must support at least:
- Fixed fractional risk per trade
- Fixed lot size
- ATR-based stop distance with position sizing from account risk
- Optional equity curve protection, such as max daily loss, max drawdown brake, or cooldown

Money management must be testable independently from signal generation.

## Execution Model Rules

Execution assumptions must be configurable and tested:
- Entry timing: next bar open by default
- Spread model: fixed or time-varying
- Slippage model: zero by default only in isolated correctness tests
- Stop and take-profit evaluation order must be explicit
- Position netting or non-netting mode must be explicit
- Concurrent trade policy must be explicit

Default to conservative assumptions when uncertain.

## Validation Rules

No strategy is considered valid unless it passes all of the following:
- In-sample and out-of-sample separation
- Walk-forward validation
- Cross-pair robustness where applicable
- Sensitivity checks on key parameters
- Basic Monte Carlo robustness on trade sequence or return sequence
- Minimum trade count threshold
- Realistic cost assumptions

Add advanced controls where feasible:
- Deflated Sharpe or equivalent multiple-testing-aware score
- Probability of Backtest Overfitting, if implemented carefully
- Stability by year and by market regime

## Required Tests Before Claiming Correctness

At minimum, maintain tests for:

1. Data integrity:
   - sorted timestamps
   - no duplicates after normalization
   - timezone normalization
   - gap handling rules
   - reproducible resampling
   - Dukascopy instrument and timeframe mapping correctness
   - deterministic merge behavior across chunked downloads
   - explicit and tested price-basis metadata, such as bid, ask, mid, or provider default

2. Feature correctness:
   - rolling window alignment
   - no future leakage
   - parity against trusted indicator outputs on fixtures
   - deterministic candle pattern labeling

3. Signal correctness:
   - crossover and threshold logic
   - regime filter gating
   - signal shifting at decision time

4. Execution correctness:
   - next-bar entry
   - stop-loss and take-profit triggering
   - tie-break rules when both are touched
   - spread and slippage application
   - position sizing rounding
   - consistent treatment of price basis versus spread model

5. Portfolio correctness:
   - cash and equity updates
   - max open position rules
   - risk cap enforcement
   - multi-pair bookkeeping

6. Metrics correctness:
   - return series
   - drawdown
   - Sharpe-like metrics
   - expectancy
   - profit factor
   - win rate
   - CAGR, if appropriate for the test horizon

7. Reproducibility:
   - same config + same data + same seed => same results
   - run fingerprint changes when config or data changes

8. Anti-bias regression tests:
   - known lookahead traps
   - same-bar fill traps
   - accidental fitting on test data
   - accidental use of future volatility or future session labels

## Working Process For The Agent

When implementing or changing anything significant:

1. Read `PLANS.md` sections relevant to the task.
2. Identify the target module and explicit acceptance criteria.
3. Implement the smallest correct slice.
4. Add or update tests first or alongside the code.
5. Run lint, type checks, and tests.
6. Record assumptions in code comments or docs where needed.
7. Do not broaden scope unnecessarily.

Prefer incremental milestones over wide unreviewable changes.

## Definition of Done

A task is done only when:
- code is implemented,
- tests cover the behavior and edge cases,
- results are reproducible,
- no obvious leakage path remains,
- docs or config examples are updated if needed,
- commands run cleanly.

## Command Conventions

If these commands do not exist yet, create them and keep them stable:

- `make setup`
- `make lint`
- `make typecheck`
- `make test`
- `make test-unit`
- `make test-integration`
- `make smoke`
- `make example-run`

Expected behaviors:
- `make setup`: install dependencies and dev tools
- `make lint`: formatting and lint checks
- `make typecheck`: static type checks
- `make test`: all automated tests
- `make smoke`: quick end-to-end sanity run on tiny fixtures
- `make example-run`: one small reproducible strategy run that writes artifacts

## Preferred Tooling

Default stack unless the repository already establishes something else:
- `pandas`, `numpy`, `pyarrow`
- `dukascopy-python` for historical price downloads through an internal provider adapter
- `pandas-ta` for indicator generation, wrapped behind our own interfaces
- `pytest`
- `ruff`
- `mypy` or `pyright`
- `pydantic` for config validation if useful
- `matplotlib` or simple HTML reports for charts
- `sqlite3` or `duckdb` for run metadata
- optional acceleration only after correctness parity

Never bind business logic directly to a third-party TA library. Use an internal adapter layer so libraries can be swapped.

## Documentation Rules

- Keep `AGENTS.md` focused on durable repo rules.
- Put detailed architecture, milestone plans, schemas, and validation design in `PLANS.md`.
- Add module-level docs for non-obvious logic, especially execution and anti-leakage decisions.
- Document every assumption that materially affects backtest outcomes.

## Things The Agent Must Not Do

- Do not claim a strategy is robust based on one split or one pair.
- Do not optimize solely for total return.
- Do not skip cost modeling because it is inconvenient.
- Do not hide failing experiments.
- Do not hard-code research assumptions into production logic.
- Do not use notebooks as the source of truth for core engine behavior.
- Do not refactor away clarity in the name of cleverness.

## Escalation Guidance

If the task requires a major design choice not resolved in `PLANS.md`, prefer:
1. the option with lower leakage risk,
2. the option with greater reproducibility,
3. the option that is easier to test.

Update `PLANS.md` when a major architectural decision is settled.
