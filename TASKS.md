# TASKS.md

## Current Status

This repository is no longer at the planning-only stage.

Completed or materially implemented:

- Task 0: repository bootstrap
- Task 1: core schemas and config contracts
- Task 2: Dukascopy provider abstraction, mapping, chunk planning, and raw artifact metadata
- Task 3: canonical normalization, validation, resampling, and dataset fingerprinting
- Task 4: session labeling and explicit price-basis propagation through canonical data
- Task 5: deterministic fixture builders and fixture-backed normalization tests
- Task 6: feature engine framework
- Task 7: initial implemented feature subset:
  - SMA
  - EMA
  - RSI
  - ATR
- Task 9: strategy grammar / signal DSL foundation
- Task 10: deterministic sizing models
- Task 11: conservative execution foundation
- Task 12: portfolio/accounting foundation
- Task 13: trade/equity/grouped metrics foundation
- Task 14: run registry and duplicate detection
- Task 15: single-indicator enumeration and leaderboard foundation
- Task 17: validation split / walk-forward / Monte Carlo helpers
- Task 18: anti-bias regression suite foundation
- Task 19: reporting and warning flag foundation
- Task 20: first end-to-end vertical slice
- Task 21: multi-pair vertical slice
- Task 23: documentation and example configs
- Task 16: controlled 2-indicator and 3-indicator combination generation

Not fully implemented yet:

- Task 8: broader candlestick pattern library
- Task 22: profiling and performance tuning

Operational status:

- `ruff` passes
- `pytest` passes
- current passing test count: 112

Next agent starting point:

1. Treat the foundation build as complete.
2. If further work is required, start with Task 22.
3. Only after profiling evidence exists should any optimization change core paths.
4. Preserve parity with the current passing regression suite.

## Purpose

This file breaks the implementation of the FX systematic strategy lab into ordered, testable tasks for a coding agent.

The sequencing matters. Build from data correctness upward. Do not jump ahead to large-scale sweeps before the data, feature alignment, execution model, and anti-bias protections are proven correct.

Each task must be completed with code, tests, and documentation updates where relevant.

---

## Global execution rules

1. Read `AGENTS.md` and `PLANS.md` before starting any non-trivial task.
2. Work in small, reviewable increments.
3. Do not optimize for speed before correctness is proven.
4. Do not introduce hidden defaults.
5. Every task must include:
   - implementation
   - tests
   - config examples if relevant
   - reproducibility considerations
6. Do not mark a task complete unless its acceptance tests pass.
7. All timestamps must be handled in UTC internally.
8. All historical price downloads in v1 must go through the internal Dukascopy provider adapter built on `dukascopy-python`.

---

## Task 0: Bootstrap the repository

### Goal
Create the repository skeleton and engineering foundation.

### Deliverables
- `src/` layout
- package structure under `src/fxlab/`
- `tests/` split into `unit/`, `integration/`, `regression/`, `fixtures/`
- `pyproject.toml`
- `Makefile`
- basic logging setup
- base config loading module
- type checking and linting setup
- minimal README with local setup instructions

### Acceptance criteria
- package imports resolve cleanly
- test runner works
- lint and type checks run
- sample config can be loaded successfully

### Required tests
- config loading smoke test
- package import smoke test
- path and artifact directory creation test

---

## Task 1: Define core schemas and config contracts

### Goal
Create the typed contracts that the rest of the system will use.

### Deliverables
- typed config models for:
  - dataset download requests
  - canonical dataset manifests
  - feature jobs
  - strategy definitions
  - risk settings
  - execution settings
  - experiment runs
  - validation plans
- enums or validated string types for:
  - timeframe
  - pair
  - price basis
  - entry timing
  - position mode
- dataset fingerprint schema
- run metadata schema

### Acceptance criteria
- invalid configs fail loudly
- valid configs serialize and deserialize deterministically
- schema versioning exists where needed

### Required tests
- config validation tests
- serialization roundtrip tests
- invalid enum and missing-field rejection tests

---

## Task 2: Implement the Dukascopy provider adapter

### Goal
Make Dukascopy the canonical historical data source for v1 through one internal provider interface.

### Deliverables
- `HistoricalDataProvider` interface
- `DukascopyProvider` implementation using `dukascopy-python`
- instrument mapping layer
- timeframe mapping layer
- chunked download support
- manifest generation for each download job
- raw artifact persistence
- checksum or content-hash generation

### Acceptance criteria
- all direct provider access is isolated to provider module
- chunked downloads recombine deterministically
- raw download metadata is persisted
- provider response shapes do not leak into downstream modules

### Required tests
- instrument mapping tests
- timeframe mapping tests
- manifest creation test
- deterministic chunk merge test
- raw artifact checksum test
- mocked provider download smoke test

---

## Task 3: Build data normalization and canonical dataset creation

### Goal
Convert raw provider data into canonical bar datasets with strict invariants.

### Deliverables
- raw-to-canonical normalization pipeline
- UTC timestamp normalization
- schema validation
- duplicate handling policy
- gap detection policy
- OHLC validation
- deterministic resampling
- canonical Parquet writer
- data quality report generator

### Acceptance criteria
- canonical data conforms to required schema
- no duplicate `(pair, timeframe, timestamp)` rows remain
- invalid OHLC records are surfaced
- resampling is deterministic
- canonical dataset fingerprint is generated

### Required tests
- timestamp normalization tests
- duplicate removal behavior test
- invalid OHLC rejection test
- sortedness test
- reproducible resampling test
- dataset fingerprint determinism test

---

## Task 4: Add session labeling and price-basis handling

### Goal
Make session flags and price-basis semantics explicit and testable.

### Deliverables
- session labeling module:
  - Asia
  - London
  - New York
- explicit `price_basis` propagation through canonical data
- rules for spread interaction with bid, ask, mid, or provider default basis
- manifest fields for price basis assumptions

### Acceptance criteria
- every canonical dataset records price basis explicitly
- session labels are deterministic
- execution layer can consume basis information later without ambiguity

### Required tests
- session labeling fixture tests
- price basis metadata propagation test
- basis plus spread consistency tests

---

## Task 5: Build data fixtures for correctness testing

### Goal
Create small deterministic fixtures that make the rest of the lab testable.

### Deliverables
- tiny canonical OHLC fixture datasets
- edge-case datasets:
  - gaps
  - duplicate timestamps
  - flat bars
  - bars where stop and target could both be touched
  - session boundary transitions
- expected outputs for selected transforms

### Acceptance criteria
- fixtures are small, readable, stable, and versioned
- fixtures are sufficient to test anti-bias and execution edge cases

### Required tests
- fixture integrity tests
- fixture loading tests

---

## Task 6: Build the feature engine framework

### Goal
Create the base framework for feature computation with strict alignment rules.

### Deliverables
- feature registry
- feature job runner
- lagging and alignment helpers
- feature table writer
- feature metadata and fingerprinting
- no-leakage guardrails for rolling-window features

### Acceptance criteria
- features are keyed by `(pair, timeframe, timestamp)`
- rolling features align only to information available at decision time
- feature jobs are reproducible

### Required tests
- rolling alignment tests
- lag helper tests
- feature fingerprint determinism test
- no-future-leak regression tests

---

## Task 7: Implement the initial curated feature set

### Goal
Implement the initial v1 indicators and regime features.

### Deliverables
Initial feature set, likely including:
- SMA
- EMA
- RSI
- MACD
- ATR
- Bollinger Bands
- ADX
- Stochastic
- Donchian channels
- rolling volatility
- range compression and expansion
- session features
- basic market structure features

### Acceptance criteria
- indicators match trusted references within tolerance
- all features document parameters and output columns
- feature naming is stable and machine-readable

### Required tests
- parity tests against trusted indicator outputs on fixtures
- NaN warmup behavior tests
- parameterized indicator output tests

---

## Task 8: Implement candlestick and pattern features

### Goal
Support candlestick-based triggers and pattern filters without ambiguity.

### Deliverables
- deterministic candlestick pattern labeling framework
- initial pattern set, for example:
  - doji
  - engulfing
  - hammer
  - shooting star
  - inside bar
  - outside bar
- pattern metadata and thresholds where relevant

### Acceptance criteria
- pattern definitions are explicit, not implicit
- labels do not depend on future bars
- outputs are reproducible

### Required tests
- pattern fixture tests
- edge-case classification tests
- no-lookahead regression tests

---

## Task 9: Build the strategy grammar and signal DSL

### Goal
Express strategies as reusable building blocks rather than handwritten ad hoc scripts.

### Deliverables
- strategy config schema
- role-based components:
  - universe
  - timeframe
  - regime filter
  - setup
  - trigger
  - exit
  - sizing
  - portfolio constraints
- signal primitives:
  - cross above
  - cross below
  - threshold above
  - threshold below
  - band touch
  - breakout
  - confirmation window
- signal composition rules:
  - AND
  - OR
  - NOT
  - sequential gating if needed

### Acceptance criteria
- a strategy can be defined entirely from config
- signals are deterministic
- decision-time shifting is explicit and enforced

### Required tests
- crossover logic tests
- threshold logic tests
- composition logic tests
- decision-time signal shift tests
- regime gating tests

---

## Task 10: Implement money management models

### Goal
Separate risk logic from signal logic and make it independently testable.

### Deliverables
- fixed lot sizing
- fixed fractional risk
- ATR-based stop distance with account-risk sizing
- max per-trade risk cap
- optional equity protection rules:
  - max daily loss
  - drawdown brake
  - cooldown

### Acceptance criteria
- position size is deterministic for given inputs
- lot or unit rounding is explicit
- risk sizing can be tested independently of entries

### Required tests
- fixed lot sizing tests
- fixed fractional risk sizing tests
- ATR-based sizing tests
- risk cap enforcement tests
- equity protection rule tests

---

## Task 11: Build the execution engine

### Goal
Translate signals into realistic fills under explicit assumptions.

### Deliverables
- order model
- next-bar-open entry model
- stop-loss and take-profit handling
- tie-break rule when both stop and target are touched in same bar
- spread model support:
  - fixed spread
  - optional time-varying spread later
- slippage model support
- position mode:
  - netting
  - non-netting, if supported
- trade log output

### Acceptance criteria
- fill rules are explicit, not assumed
- same-bar fantasy fills are not allowed by default
- stop and target ordering logic is documented and tested

### Required tests
- next-bar entry tests
- stop-loss trigger tests
- take-profit trigger tests
- same-bar stop/target tie-break tests
- spread application tests
- slippage application tests
- price basis plus spread interaction tests

---

## Task 12: Build the portfolio simulator

### Goal
Track account state across trades and pairs correctly.

### Deliverables
- cash accounting
- equity curve generation
- open position tracking
- max open trades rule
- per-pair risk cap
- multi-pair bookkeeping
- portfolio-level event log

### Acceptance criteria
- equity and cash evolve consistently
- multiple pairs can be simulated correctly
- constraints are enforced at the portfolio level

### Required tests
- cash and equity update tests
- max open position tests
- per-pair cap tests
- multi-pair bookkeeping tests

---

## Task 13: Implement metrics and evaluation

### Goal
Compute reliable performance and risk metrics for strategies and runs.

### Deliverables
- return series
- drawdown series
- profit factor
- expectancy
- win rate
- average trade
- Sharpe-like metrics
- CAGR where appropriate
- metrics by:
  - full run
  - year
  - pair
  - regime
  - split

### Acceptance criteria
- metric formulas are explicit and documented
- metrics are deterministic
- metrics can be recomputed from trade logs and equity curve

### Required tests
- metric fixture tests
- drawdown correctness tests
- expectancy and profit factor tests
- split and subgroup aggregation tests

---

## Task 14: Build experiment storage and run registry

### Goal
Make every experiment reproducible and queryable.

### Deliverables
- run registry in SQLite or DuckDB
- run metadata persistence
- config hash storage
- dataset fingerprint storage
- code version capture
- random seed capture
- artifact path storage
- duplicate run prevention or detection
- failed run recording

### Acceptance criteria
- identical runs can be detected
- failed trials are not silently dropped
- every leaderboard row points back to exact inputs

### Required tests
- run registration tests
- duplicate detection tests
- failed run persistence tests
- reproducibility metadata completeness tests

---

## Task 15: Implement single-indicator sweep runner

### Goal
Run controlled systematic experiments over single indicators first.

### Deliverables
- single-indicator experiment enumerator
- standardized execution and risk framework
- result aggregation
- leaderboard generation
- artifact output for each run

### Acceptance criteria
- indicator sweeps are config-driven
- results are reproducible
- ranking supports more than raw return

### Required tests
- sweep enumeration tests
- artifact creation tests
- deterministic rerun tests
- leaderboard generation tests

---

## Task 16: Implement selected 2-indicator and 3-indicator combination sweeps

### Goal
Expand the search space carefully, only after single-indicator framework is proven.

### Deliverables
- role-aware combination generator
- redundancy filtering rules
- constraints that discourage meaningless combinations
- result aggregation for pair and triple combinations

### Acceptance criteria
- combinations respect distinct indicator roles where possible
- combinatorial explosion is controlled through config and filters
- failing combinations are recorded, not discarded

### Required tests
- combination generator tests
- redundancy filter tests
- config-bound search-space tests

---

## Task 17: Build the validation framework

### Goal
Reject fragile strategies and reduce false discoveries.

### Deliverables
- in-sample and out-of-sample split utilities
- walk-forward runner
- parameter sensitivity checks
- trade-sequence or return-sequence Monte Carlo
- minimum trade-count filter
- realistic cost stress tests
- optional advanced metrics:
  - deflated Sharpe
  - multiple-testing-aware score
  - probability of backtest overfitting, only if implemented carefully

### Acceptance criteria
- final test segment is never used for selection
- walk-forward outputs are reproducible
- validation reports clearly separate selection from final evaluation

### Required tests
- split isolation tests
- walk-forward correctness tests
- sensitivity analysis smoke tests
- Monte Carlo determinism under fixed seed
- anti-test-data-leak regression tests

---

## Task 18: Build anti-bias regression suite

### Goal
Create explicit traps so the engine proves it is not cheating accidentally.

### Deliverables
Regression tests for:
- lookahead bias via unshifted rolling features
- same-bar entry and exit fantasy fills
- future volatility usage
- future session label usage
- accidental fitting on final test segment
- accidental reuse of out-of-sample metrics during ranking
- provider or dataset mismatch across runs

### Acceptance criteria
- the suite fails when a bias is deliberately reintroduced
- anti-bias tests are part of default CI

### Required tests
- one regression test per known failure mode above

---

## Task 19: Reporting and leaderboard outputs

### Goal
Make results inspectable, not just stored.

### Deliverables
- leaderboard tables
- scorecards
- by-year breakdowns
- by-pair breakdowns
- by-regime breakdowns
- experiment summary reports
- validation summary reports
- clear warnings when trade count is too low or robustness fails

### Acceptance criteria
- reports are traceable to run IDs and config hashes
- unstable strategies are visibly flagged
- ranking is not based on return alone

### Required tests
- report generation smoke tests
- leaderboard schema tests
- warning flag tests

---

## Task 20: End-to-end vertical slice

### Goal
Prove the full lab works on one small but real workflow.

### Deliverables
One end-to-end pipeline that:
1. downloads one pair from Dukascopy
2. normalizes to canonical bars
3. computes a small feature set
4. builds one config-defined strategy
5. backtests it
6. computes metrics
7. records the run
8. produces a summary report

Suggested initial slice:
- pair: EURUSD
- timeframe: 1H
- period: small fixed window
- strategy: simple EMA trend filter plus RSI trigger plus ATR stop sizing

### Acceptance criteria
- the whole pipeline runs from config
- rerunning with same inputs gives same outputs
- all artifacts are produced and linked
- no leakage or same-bar fill violations occur

### Required tests
- end-to-end integration test
- deterministic rerun test
- artifact completeness test

---

## Task 21: Multi-pair end-to-end experiment

### Goal
Prove the lab works beyond a single pair.

### Deliverables
- same vertical slice extended to all initial 6 major pairs
- pair-aware result aggregation
- cross-pair comparison report

### Acceptance criteria
- multi-pair bookkeeping is correct
- results can be broken down by pair and aggregated portfolio-wide
- per-pair constraints are enforced

### Required tests
- multi-pair integration test
- pair-level and aggregate consistency tests

---

## Task 22: Performance tuning only after parity is proven

### Goal
Improve runtime without changing outputs.

### Current status
Not started. This is now the primary remaining top-level task.

### Deliverables
- profiling results
- bottleneck analysis
- selective optimization, vectorization, caching, or parallel execution
- parity checks between optimized and reference paths

### Acceptance criteria
- optimized path matches reference outputs exactly or within documented tolerances
- optimizations do not bypass logging, reproducibility, or validation

### Required tests
- optimized vs reference parity tests
- cache correctness tests

---

## Task 23: Documentation and examples

### Goal
Make the system usable by a human researcher and reliable for future agent work.

### Current status
Foundation completed:
- `README.md` updated
- architecture and troubleshooting docs added
- example configs added and validated by tests

### Deliverables
- updated README
- architecture overview in `docs/`
- config examples for:
  - dataset download
  - feature job
  - single-indicator strategy
  - 2-indicator strategy
  - validation plan
- troubleshooting guide
- assumptions guide for spread, price basis, and execution

### Acceptance criteria
- a new developer can run the vertical slice from docs alone
- documentation matches actual commands and config structure

### Required tests
- docs command smoke tests where feasible
- config example validation tests

---

## Final acceptance gate for v1

Do not claim v1 is complete until all of the following are true:

1. Historical downloads are performed only through the internal Dukascopy adapter.
2. Canonical datasets are reproducible from raw data plus preprocessing version.
3. Feature alignment is tested and free of obvious future leakage.
4. Strategy definitions are config-driven.
5. Execution assumptions are explicit and tested.
6. Money management is independent and tested.
7. Single-indicator sweeps work end-to-end.
8. Selected multi-indicator sweeps work end-to-end.
9. Validation separates selection from final testing.
10. Results are reproducible and fully traceable.
11. Anti-bias regression tests are green.
12. Reports clearly flag low-trade-count or fragile strategies.

---

## Suggested implementation order

1. Task 0
2. Task 1
3. Task 2
4. Task 3
5. Task 4
6. Task 5
7. Task 6
8. Task 7
9. Task 8
10. Task 9
11. Task 10
12. Task 11
13. Task 12
14. Task 13
15. Task 14
16. Task 15
17. Task 17
18. Task 18
19. Task 19
20. Task 20
21. Task 16
22. Task 21
23. Task 22
24. Task 23

Reason for this order:
- get data and correctness foundations first
- prove one clean vertical slice
- only then widen the search space
- only then optimize performance

---

## Notes for the coding agent

1. Prefer one small merged PR-sized slice at a time.
2. When uncertain, choose the more conservative execution assumption.
3. Never silently “fix” invalid data without logging the action.
4. Never drop failed experiments from the registry.
5. Never use final out-of-sample results to guide selection logic.
6. If a feature or strategy rule risks leakage, add a regression test before proceeding.
