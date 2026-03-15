# PLANS.md

## Purpose

This document is the full technical blueprint for building a research-grade FX systematic strategy lab.

It exists to help a coding agent implement the repository with minimal ambiguity and maximum resistance to false conclusions. The lab is for systematic idea discovery, fair comparison, and rigorous validation. It is not a promise that profitable strategies will emerge from brute-force search.

`AGENTS.md` contains durable operating rules. This file contains the architecture, milestones, schemas, experiment flow, validation logic, and acceptance criteria.

## Status Snapshot

Current repository status as of this implementation pass:

- Core foundation is implemented and validated.
- `ruff` passes.
- `pytest` passes.
- The repository currently has 112 passing tests.
- A mocked but full end-to-end vertical slice exists, including:
  - provider request path
  - raw artifact and manifest write
  - canonical normalization
  - feature computation
  - strategy evaluation
  - conservative execution
  - portfolio/accounting update
  - metrics and reporting output
  - run registry persistence
- A multi-pair vertical slice also exists.

Implemented foundation areas:

- repository bootstrap and tooling
- typed configs and core domain models
- Dukascopy provider contract, mapping, chunk planning, and raw manifest support
- canonical dataset normalization, validation, resampling, fingerprinting, and quality summaries
- UTC session labeling and deterministic fixtures
- feature engine foundation with `SMA`, `EMA`, `RSI`, and `ATR`
- strategy DSL foundation with primitive predicates and boolean composition
- conservative long-only execution foundation
- risk sizing foundation
- portfolio/accounting foundation
- metrics foundation
- SQLite run registry
- single-indicator candidate enumeration and leaderboard ranking
- validation split / walk-forward / Monte Carlo helpers
- anti-bias regression suite
- reporting helpers
- single-pair and multi-pair vertical slices
- documentation and example configs
- controlled 2-indicator and 3-indicator combination generation

Known current limitation:

- live `dukascopy-python` network integration is not yet wired into the end-to-end slice; the current pipeline uses injected deterministic fetchers for end-to-end tests.

Primary remaining top-level task:

- `Task 22`: performance tuning only after parity remains stable

---

## 1. Objectives

### 1.1 Core goals

Build a lab that can:

1. Load and normalize historical FX market data for a defined universe.
2. Compute indicators, candle patterns, market structure, and regime features.
3. Express strategies as config-driven combinations of reusable building blocks.
4. Simulate trades under realistic execution and money management assumptions.
5. Run structured sweeps over:
   - single indicators,
   - selected 2-indicator combinations,
   - selected 3-indicator combinations.
6. Rank and compare strategies using risk-aware metrics.
7. Validate candidate strategies using out-of-sample and walk-forward procedures.
8. Persist enough metadata to reproduce every result exactly.

### 1.2 Initial operating scope

Start narrow:

- Asset class: spot FX or FX-CFD historical bars
- Historical source: Dukascopy Historical Data Feed via `dukascopy-python`
- Universe:
  - EURUSD
  - GBPUSD
  - USDJPY
  - AUDUSD
  - USDCAD
  - USDCHF
- Timeframes:
  - initial: 1H
  - later: 15m, 4H, Daily
- History:
  - initial: 3 years
  - later: 5 to 10 years
- Starting capital:
  - default: USD 500
- Risk model:
  - default: fixed fractional risk with ATR-based stop
- Search scope:
  - initial: 20 to 30 curated indicators
  - later: larger library via adapters

### 1.3 Non-goals for v1

Do not attempt all of the following in v1:
- Tick-accurate execution
- Full broker integration
- Live trading
- Genetic programming
- Reinforcement learning
- Unbounded search across all parameters and all indicators
- Production-grade UI

---

## 2. Design principles

1. Correctness before scale.
2. Explicit assumptions beat hidden defaults.
3. Separate concerns cleanly.
4. Everything important is configurable and logged.
5. Every result must be reproducible.
6. Research must be robust to overfitting pressure.
7. The engine must make it hard to cheat accidentally.

---

## 3. High-level system architecture

The system should be split into the following layers.

### 3.1 Data layer

Responsibilities:
- download raw historical data through a single internal Dukascopy provider adapter built on `dukascopy-python`
- persist raw provider artifacts and manifests
- validate shape and timestamp consistency
- normalize schema
- convert timezone to UTC
- resample where needed
- enrich with trading session labels
- persist canonical datasets

Outputs:
- canonical bar data
- data quality report
- dataset fingerprint

### 3.1.1 Dukascopy provider requirements

The repository must treat Dukascopy as the canonical historical market data source for v1.

Implementation rules:
- create an internal provider interface, for example `HistoricalDataProvider`
- implement `DukascopyProvider` using `dukascopy-python`
- keep all direct provider calls isolated to the data provider module
- support chunked downloads for long ranges and deterministic recombination
- persist a manifest for every download job
- never let downstream modules depend directly on provider-specific response shapes

Each download manifest should record at minimum:
- provider name
- `dukascopy-python` package version
- pair or instrument requested
- provider interval requested
- requested start and end timestamps
- retrieval timestamp
- local raw artifact paths
- checksum or content hash for each raw artifact
- normalization or preprocessing version
- declared price basis if known

Design intent:
- raw downloads are immutable source artifacts
- canonical datasets are reproducible derived artifacts
- the lab can later add other providers without changing the rest of the engine

### 3.2 Feature layer

Responsibilities:
- compute indicators
- compute candle patterns
- compute market structure and volatility features
- compute session and regime features
- enforce feature alignment and lagging rules

Outputs:
- feature tables keyed by `(pair, timeframe, timestamp)`

### 3.3 Strategy definition layer

Responsibilities:
- represent strategies as configurations, not handwritten logic
- combine features into setup, trigger, filter, and exit rules
- support role-based indicator composition

Outputs:
- deterministic signal tables
- strategy config hash

### 3.4 Execution and portfolio layer

Responsibilities:
- convert signals into orders and positions
- apply spread and slippage
- compute stop and target logic
- enforce money management and portfolio rules
- maintain cash, equity, margin, and open positions

Outputs:
- trades
- position timeline
- equity curve
- execution logs

### 3.5 Evaluation layer

Responsibilities:
- compute performance metrics
- evaluate by year, pair, regime, and split
- store rankings and diagnostic summaries

Outputs:
- metrics tables
- scorecards
- summary reports

### 3.6 Validation layer

Responsibilities:
- split data without leakage
- walk-forward evaluation
- parameter sensitivity
- Monte Carlo
- multiple-testing-aware ranking

Outputs:
- robustness verdicts
- validation reports
- shortlisted candidates

### 3.7 Orchestration layer

Responsibilities:
- enumerate experiment definitions
- schedule and run experiments
- persist configs and results
- prevent duplicate runs
- allow resume and re-run

Outputs:
- run registry
- reproducible artifacts
- leaderboard tables

---

## 4. Repository layout

Recommended layout:

```text
.
├── AGENTS.md
├── PLANS.md
├── README.md
├── Makefile
├── pyproject.toml
├── configs/
│   ├── datasets/
│   ├── features/
│   ├── strategies/
│   ├── sweeps/
│   └── validation/
├── docs/
├── data/
│   ├── raw/
│   ├── interim/
│   ├── canonical/
│   └── fixtures/
├── outputs/
│   ├── runs/
│   ├── reports/
│   └── leaderboards/
├── src/
│   └── fxlab/
│       ├── config/
│       ├── data/
│       ├── features/
│       ├── signals/
│       ├── execution/
│       ├── risk/
│       ├── backtest/
│       ├── metrics/
│       ├── validation/
│       ├── experiments/
│       ├── storage/
│       └── reporting/
└── tests/
    ├── unit/
    ├── integration/
    ├── regression/
    └── fixtures/
```

---

## 5. Canonical data model

### 5.1 Source-of-truth and provider staging

The lab should distinguish clearly between:
- raw provider downloads from Dukascopy
- normalized canonical datasets used by the rest of the system

Rules:
- raw Dukascopy data must be stored unchanged or as lossless provider-normalized files plus manifest
- canonical bars must be reproducible from raw files and preprocessing code version
- the system must never silently mix datasets pulled with different provider assumptions
- any aggregation from ticks to bars must be deterministic and tested

### 5.2 Canonical bar schema

Each canonical bar should include at minimum:

- `pair`: string, for example `EURUSD`
- `timeframe`: string, for example `1H`
- `timestamp`: timezone-aware UTC timestamp
- `open`: float
- `high`: float
- `low`: float
- `close`: float
- `volume`: float or nullable if unavailable
- `tick_volume`: float or nullable
- `spread`: float or nullable
- `source`: string
- `provider`: string, initially `dukascopy`
- `source_instrument`: string or nullable if different from canonical pair naming
- `price_basis`: enum-like string such as `bid`, `ask`, `mid`, or `provider_default`
- `is_complete_bar`: bool
- `session_asia`: bool
- `session_london`: bool
- `session_newyork`: bool

Rules:
- sorted ascending by timestamp
- unique by `(pair, timeframe, timestamp)`
- no negative prices or invalid OHLC order
- explicit missing-bar handling policy

### 5.3 Dataset fingerprint

Each canonical dataset should have a fingerprint generated from:
- source name
- provider manifest hash or raw artifact hash set
- pair
- timeframe
- start/end timestamp
- row count
- hash of stable serialized content or file-level content hash
- preprocessing version

The fingerprint must be stored with every run.

---

## 6. Feature catalog

### 6.1 Feature categories for initial scope

Do not start with every possible indicator. Start with a curated, representative set.

#### Trend
- SMA
- EMA
- WMA
- HMA
- MACD
- ADX
- Supertrend
- Ichimoku components, later if desired

#### Momentum
- RSI
- Stochastic
- Stochastic RSI
- CCI
- ROC
- Momentum

#### Volatility
- ATR
- NATR
- Bollinger Bands
- Keltner Channels
- Donchian Channels

#### Mean reversion / bands
- Z-score of returns or price distance
- Bollinger percentile
- Distance from moving average

#### Volume / liquidity proxies
For FX, centralized true volume is usually unavailable in spot data. Use:
- tick volume if available from Dukascopy or derived bars
- spread
- rolling range compression / expansion
- session labels
- bar overlap and volatility proxies

#### Market structure
- rolling swing highs and lows
- breakout state
- range state
- trend slope
- consolidation flags

#### Candle patterns
Treat candle patterns as secondary signals or filters unless evidence shows otherwise.
Initial list:
- doji
- engulfing
- hammer / shooting star
- inside bar
- outside bar
- pin bar heuristic, if defined clearly

### 6.2 Feature computation rules

- Every feature must define:
  - required input columns
  - warmup bars
  - whether the result must be shifted before use
  - missing value policy
  - parameter schema
- Wrap third-party indicator libraries behind internal adapters.
- Feature outputs must be deterministic.
- Feature parity tests must compare against trusted fixture values.

### 6.3 Feature storage

Preferred pattern:
- compute canonical features into Parquet keyed by pair and timeframe
- optional cache by `(dataset_fingerprint, feature_spec_hash)`

---

## 7. Strategy specification model

A strategy must be config-driven and serializable.

### 7.1 Strategy roles

Each strategy config should express:

- `name`
- `pair_universe`
- `timeframe`
- `feature_set`
- `regime_filters`
- `setup_rules`
- `entry_trigger_rules`
- `exit_rules`
- `sizing_rule`
- `portfolio_constraints`
- `cost_model`
- `validation_plan`
- `tags`

### 7.2 Rule grammar

Define a small internal rule language or structured config format.

Examples of primitive predicates:
- `crosses_above(a, b)`
- `crosses_below(a, b)`
- `greater_than(a, value_or_feature)`
- `less_than(a, value_or_feature)`
- `between(a, low, high)`
- `rising(a, lookback)`
- `falling(a, lookback)`
- `within_session("london")`
- `volatility_above(percentile_threshold)`
- `pattern_is("doji")`

Combinators:
- `all_of`
- `any_of`
- `not`

### 7.3 Example strategy shape

```yaml
name: ema_rsi_pullback
pair_universe: [EURUSD]
timeframe: 1H
feature_set:
  - ema(length=50)
  - rsi(length=14)
  - atr(length=14)
regime_filters:
  all_of:
    - greater_than(close, ema_50)
setup_rules:
  all_of:
    - less_than(rsi_14, 35)
entry_trigger_rules:
  all_of:
    - crosses_above(rsi_14, 35)
exit_rules:
  stop:
    type: atr_multiple
    multiple: 1.5
  take_profit:
    type: risk_reward
    multiple: 2.0
  time_exit:
    bars: 24
sizing_rule:
  type: fixed_fractional_atr
  risk_fraction: 0.01
portfolio_constraints:
  max_open_positions: 1
cost_model:
  spread_mode: fixed
  spread_pips: 1.2
  slippage_pips: 0.2
validation_plan: standard_walk_forward
tags: [trend, momentum, pullback]
```

---

## 8. Search-space design

### 8.1 Why not brute-force everything

Blind exhaustive search across all indicators, all parameters, and all combinations will create:
- huge computational cost
- severe multiple testing problems
- false positives that look good by luck

Therefore, the search must be staged.

### 8.2 Search stages

#### Stage A: Single-indicator baselines
For each indicator or pattern:
- use standardized entry and exit templates
- use a small curated parameter set
- run across initial pairs and timeframe
- record all failures and low-trade cases

Purpose:
- estimate whether the indicator contributes signal at all

#### Stage B: Pair combinations
Only combine components that pass minimum quality thresholds in Stage A, or that fill distinct strategy roles.

Allowed role pairings:
- trend + trigger
- trend + volatility filter
- mean-reversion + regime filter
- structure + trigger

Discourage:
- trend + trend
- momentum + momentum
unless explicitly justified

#### Stage C: Triple combinations
Only allow triples when each part serves a distinct role:
- regime filter
- setup
- trigger

This limits redundancy and search explosion.

### 8.3 Parameter policy

Use curated parameter sets, not huge grids.

Example:
- EMA: [20, 50, 100]
- RSI length: [7, 14, 21]
- ATR multiple: [1.0, 1.5, 2.0]
- RR target: [1.0, 1.5, 2.0]

Add more values only when a narrower hypothesis merits deeper study.

---

## 9. Money management and risk model

### 9.1 Initial supported sizing methods

1. Fixed lot:
   - simplest baseline
2. Fixed fractional:
   - risk a fixed fraction of current equity
3. Fixed fractional with ATR stop:
   - position size derived from entry, stop distance, and account risk
4. Volatility-targeted sizing, later

### 9.2 Initial supported exits

- fixed stop in pips
- ATR-multiple stop
- fixed take-profit in pips
- risk-reward target
- trailing ATR stop
- time-based exit
- opposite-signal exit

### 9.3 Portfolio guardrails

At minimum support:
- max open positions
- max positions per pair
- max portfolio risk
- cooldown after stop-out, optional
- equity drawdown brake, optional

### 9.4 Small-account realism

Default initial capital is USD 500. Therefore:
- enforce minimum trade size assumptions explicitly
- support fractional lots or broker-compatible position granularity assumptions
- surface when a strategy is infeasible due to lot-size constraints
- distinguish theoretical risk sizing from executable sizing

---

## 10. Execution model

### 10.1 Default execution assumptions

- Signal calculated on bar close
- Entry occurs at next bar open
- Spread applied at entry and exit
- Slippage applied per fill
- Stops and targets evaluated against subsequent bars only
- Long and short behavior symmetrical unless stated otherwise

### 10.2 Same-bar ambiguity handling

A common false-result source is when both stop and target appear to have been touched within the same bar after entry.

Policy options:
1. pessimistic: assume adverse fill first
2. optimistic: assume favorable fill first
3. deterministic rule by distance from open
4. intrabar data, if available

Default:
- use pessimistic mode for safety
- expose this policy in config
- test it thoroughly

### 10.3 Cost model

Support:
- fixed spread
- time-varying spread if present in data
- fixed slippage
- optional session-dependent slippage later

Never omit costs in comparative leaderboards unless the run is explicitly marked frictionless for debugging only.

### 10.4 Price-basis policy

Because Dukascopy data may be obtained as ticks or aggregated intervals, the lab must make price basis explicit.

Rules:
- every canonical dataset must declare `price_basis`
- signal generation may use one declared basis, but execution must respect the chosen spread model
- do not pretend bid-ask realism exists when only one-sided or provider-default bars are available
- if mid-based bars are used for signals and backtests, spread and slippage assumptions must be applied explicitly and consistently
- if side-aware bid and ask execution is added later, it must be treated as a separate validated execution mode

---

## 11. Validation and anti-false-results framework

This is the most important section of the entire project.

### 11.1 Biases the lab must defend against

1. Lookahead bias
2. Data leakage across train / validation / test
3. Survivorship bias, low relevance for major FX pairs but keep the design honest
4. Execution fantasy, such as same-bar fills using impossible information
5. Multiple testing bias
6. Selection bias, picking only attractive backtests
7. Regime dependence hidden by aggregate metrics
8. Parameter brittleness
9. Infeasible sizing or ignoring lot-size constraints
10. Data snooping from repeated reruns without a locked final test

### 11.2 Required split protocol

Initial default:
- training: oldest 60 percent
- validation: next 20 percent
- final test: newest 20 percent

Alternative for longer data:
- rolling walk-forward windows

Rules:
- feature warmup may use prior bars inside the same split only
- no threshold tuning on final test
- final test exists only for the top shortlisted candidates

### 11.3 Walk-forward design

Initial walk-forward approach:
- train window: 18 months
- validation window: 6 months
- step size: 3 months
- optional final locked test after walk-forward selection

For each fold:
- generate candidate settings on train
- score on validation
- carry chosen configuration forward
- aggregate fold-level metrics

### 11.4 Cross-pair robustness

A strategy should be examined on:
- the pair it was discovered on
- other major pairs in the same timeframe
- pooled portfolio behavior when appropriate

A strategy that only works on one pair should be labeled pair-specific unless justified by market structure.

### 11.5 Regime robustness

Create simple regime tags, such as:
- high volatility
- low volatility
- trend up
- trend down
- range / compression
- Asia / London / New York session

Evaluate metrics by regime to detect hidden fragility.

### 11.6 Parameter sensitivity

For shortlisted strategies:
- perturb key parameters locally
- check whether performance degrades gracefully
- reject razor-edge parameterizations

### 11.7 Monte Carlo

At minimum implement one of:
- trade sequence reshuffle
- bootstrap returns or trades with replacement

Use it to estimate variability in drawdown and ending equity.

### 11.8 Multiple-testing-aware scoring

This is optional for earliest milestones but should be planned.

Potential additions:
- Deflated Sharpe Ratio
- White's Reality Check
- Probability of Backtest Overfitting

Only implement these if done carefully and tested. Poor implementation is worse than omission.

---

## 12. Metrics and ranking

### 12.1 Required metrics

Per run:
- net return
- annualized return where meaningful
- max drawdown
- Calmar ratio
- Sharpe ratio
- Sortino ratio
- profit factor
- expectancy per trade
- average win
- average loss
- win rate
- payoff ratio
- number of trades
- exposure time
- average holding period
- consecutive wins / losses
- drawdown duration

### 12.2 Segmented metrics

Also compute by:
- year
- pair
- long vs short
- session
- volatility regime
- train / validation / test split

### 12.3 Ranking policy

Never rank by net return alone.

Recommended composite ranking:
- profitability score
- drawdown penalty
- stability score
- trade-count adequacy
- out-of-sample score
- cross-pair robustness score
- cost sensitivity penalty
- parameter brittleness penalty

All composite scores must expose their component weights.

---

## 13. Storage and reproducibility

### 13.1 Run registry

Every run must persist:
- run id
- timestamp
- git commit hash if available
- dataset fingerprint
- strategy config hash
- validation plan id
- random seed
- execution model id
- result summary
- artifact paths

### 13.2 Suggested persistence pattern

- Parquet:
  - canonical data
  - features
  - trades
  - equity curves
  - fold-level metrics
- SQLite or DuckDB:
  - run metadata
  - strategy registry
  - leaderboard summaries

### 13.3 Idempotency

If a run with the same full configuration and dataset already exists:
- skip or mark as cached
- do not silently overwrite
- allow forced rerun with a flag

---

## 14. Configuration system

Use structured configuration files.

### 14.1 Config domains

- dataset configs
- feature specs
- strategy templates
- sweep definitions
- validation plans
- reporting definitions

### 14.2 Config validation

Use a typed schema:
- dataclasses + manual validation, or
- pydantic models

Reject invalid configs early with clear errors.

---

## 15. Reporting and diagnostics

### 15.1 Minimum artifacts per run

- config snapshot
- metrics summary JSON or CSV
- trade log
- equity curve series
- drawdown series
- per-year metrics
- per-split metrics

### 15.2 Minimum leaderboard outputs

- top candidates by composite score
- top candidates by out-of-sample performance
- top candidates by cross-pair stability
- rejected candidates with rejection reasons

### 15.3 Debugging artifacts

For smoke and regression runs, produce:
- compact log
- first few signals
- first few trades
- assertion-friendly summaries

---

## 16. Testing strategy

Tests are not optional. They are the mechanism that stops false results.

### 16.1 Unit tests

#### Data tests
- canonical schema validation
- timezone conversion
- duplicate removal or rejection behavior
- invalid OHLC detection
- resampling correctness

#### Feature tests
- rolling alignment
- expected NaN warmup region
- shift behavior
- parity with small trusted fixtures
- deterministic output given same inputs

#### Rule engine tests
- primitive predicate logic
- combinator logic
- serialization / deserialization stability
- config validation failures

#### Execution tests
- next-bar entry price
- cost application
- stop and target handling
- same-bar ambiguity policy
- partial fills if implemented
- rounding to lot size

#### Risk tests
- fixed fractional sizing
- ATR-based position sizing
- max risk cap
- drawdown brake

#### Metrics tests
- drawdown
- expectancy
- Sharpe / Sortino
- profit factor
- annualization conventions

### 16.2 Integration tests

Small fixture datasets should verify:
- end-to-end single-strategy backtest
- reproducible experiment sweep
- walk-forward execution
- leaderboard generation
- report artifact writing

### 16.3 Regression tests

Create known-good fixture runs where outputs are frozen:
- exact trade count
- exact first N trades
- exact ending equity within tight tolerance
- exact key metrics within tolerance

These should catch accidental logic drift.

### 16.3.1 Provider-specific ingestion tests for Dukascopy

These are mandatory while Dukascopy remains the canonical source.

- instrument mapping test: requested pair maps to the expected provider instrument and canonical pair
- interval mapping test: requested canonical timeframe maps correctly to provider interval or aggregation path
- chunk merge test: adjacent download chunks recombine without gaps or overlaps beyond declared market closures
- manifest completeness test: provider version, request range, hashes, and raw paths are recorded
- reproducibility test: the same immutable raw artifacts normalize to the same canonical dataset fingerprint
- price-basis declaration test: every canonical dataset declares basis explicitly and downstream modules read it

### 16.4 Anti-bias tests

These are mandatory.

#### Lookahead trap fixture
Construct a fixture where using future data would obviously inflate results. The correct engine must not profit unrealistically.

#### Same-bar trap fixture
Construct bars where stop and target are both touched after entry. Verify pessimistic resolution.

#### Leakage trap
Create separate train and test windows where an intentionally leaked feature would improve results. Ensure the actual pipeline cannot access it.

#### Cost sensitivity trap
A strategy that is profitable with zero costs but unprofitable with realistic costs should be flagged, not promoted.

#### Lot-size feasibility trap
A strategy requiring micro position granularity that is impossible under chosen broker constraints should be flagged infeasible.

### 16.5 Property tests, optional but valuable

Use property-based tests for invariants:
- equity should update consistently with trade PnL
- no trade exit can occur before entry
- max drawdown is never positive
- timestamps remain sorted after pipeline transforms

---

## 17. Acceptance criteria by module

### 17.1 Data module acceptance
- downloads raw data through the Dukascopy provider adapter
- stores raw manifests and immutable source artifacts
- loads raw files into canonical schema
- validates timestamps and OHLC consistency
- writes canonical Parquet
- computes dataset fingerprint
- unit tests cover edge cases

### 17.2 Feature module acceptance
- indicator adapter interface exists
- at least 10 initial features implemented
- features align correctly with no leakage
- candle patterns supported in a deterministic way
- fixture parity tests pass

### 17.3 Signal module acceptance
- rule grammar implemented
- strategies load from config
- single-indicator strategies can be expressed without custom code
- combination logic works and is tested

### 17.4 Execution module acceptance
- next-bar execution works
- spread and slippage applied
- stop / target / time-exit policies implemented
- same-bar ambiguity policy explicit and tested

### 17.5 Risk module acceptance
- fixed lot and fixed fractional supported
- ATR-based stop sizing supported
- portfolio risk caps enforced
- infeasible size detection handled

### 17.6 Backtest module acceptance
- full trade ledger produced
- equity curve produced
- deterministic results
- integration tests pass

### 17.7 Validation module acceptance
- train / validation / test split supported
- walk-forward supported
- per-fold metrics saved
- shortlisted candidate logic implemented

### 17.8 Reporting module acceptance
- per-run artifact bundle generated
- leaderboard generated
- rejection reasons visible

---

## 18. Implementation roadmap

### Milestone 0: Repository bootstrap
Deliverables:
- pyproject
- src layout
- Makefile
- lint, typecheck, test commands
- base config schema
- logging setup

Exit criteria:
- empty smoke command works
- CI-ready local commands exist

### Milestone 1: Canonical data pipeline
Deliverables:
- Dukascopy provider adapter using `dukascopy-python`
- chunked historical download workflow and manifests
- raw file loader
- canonical schema
- validation and normalization
- Parquet writer
- dataset fingerprint
- fixture datasets

Exit criteria:
- canonical data artifacts produced for one pair
- data tests pass

### Milestone 2: Core feature engine
Deliverables:
- feature adapter interface
- first indicator set, for example EMA, SMA, RSI, ATR, MACD, Bollinger, ADX
- candle pattern heuristics
- cached feature computation

Exit criteria:
- feature tables reproducible
- parity tests pass

### Milestone 3: Rule engine and strategy config
Deliverables:
- predicate grammar
- YAML strategy configs
- parser and validator
- signal generation pipeline

Exit criteria:
- at least 5 example strategies defined fully by config

### Milestone 4: Backtest and execution engine
Deliverables:
- next-bar entries
- spread and slippage
- stop / target / time exits
- fixed lot and fixed fractional sizing
- trade log and equity curve

Exit criteria:
- end-to-end single strategy backtest on fixtures passes regression tests

### Milestone 5: Experiment runner
Deliverables:
- single-indicator sweep runner
- run registry
- artifact persistence
- basic leaderboard

Exit criteria:
- can run single-indicator sweep over 6 pairs on a sample dataset

### Milestone 6: Validation layer
Deliverables:
- train / validation / test split
- walk-forward engine
- parameter sensitivity checks
- Monte Carlo module

Exit criteria:
- shortlisted candidates carry validation artifacts

### Milestone 7: Combination search
Deliverables:
- pair-combination generator with role constraints
- triple-combination generator with role constraints
- redundancy filters
- expanded leaderboards

Exit criteria:
- combination runs complete without search explosion or silent skipping

### Milestone 8: Reporting and diagnostics
Deliverables:
- summary tables
- per-year diagnostics
- regime diagnostics
- rejection reason audit trail

Exit criteria:
- a researcher can inspect why a strategy was promoted or rejected

---

## 19. Initial strategy templates to include

These are not assumed profitable. They are baseline hypotheses.

1. Trend pullback:
   - trend filter: price above EMA
   - trigger: RSI recovery from oversold
   - exit: ATR stop, RR target

2. Mean reversion band fade:
   - setup: close below lower Bollinger
   - filter: low ADX
   - exit: mean reversion to middle band

3. Breakout:
   - setup: Donchian breakout
   - filter: rising ATR or ADX
   - exit: trailing ATR

4. Structure plus candle:
   - setup: higher timeframe trend up
   - trigger: bullish engulfing at pullback zone
   - exit: swing low stop, fixed RR

5. Session breakout:
   - setup: Asian range defined
   - trigger: London breakout
   - exit: ATR or opposite range side

Each template should have config examples and smoke-test coverage.

---

## 20. Performance and scaling guidance

Only optimize after correctness.

### 20.1 Early-stage performance priorities
- correctness
- deterministic behavior
- simple data structures
- compact fixtures

### 20.2 Later-stage scaling options
- vectorized computations
- caching
- multiprocessing across runs
- DuckDB queries for aggregation
- optional Numba or compiled helpers

### 20.3 Performance guardrail
Any optimized path must match the reference implementation on regression fixtures before replacement.

---

## 21. Suggested developer commands

Create and maintain these commands:

```bash
make setup
make lint
make typecheck
make test
make test-unit
make test-integration
make smoke
make example-run
```

Expected meanings:
- `make setup`: install package and dev dependencies
- `make lint`: formatting and lint checks
- `make typecheck`: static type checks
- `make test`: full suite
- `make smoke`: minimal end-to-end run on tiny fixture
- `make example-run`: reproducible example writing artifacts to `outputs/`

---

## 22. Definition of trustworthy output

A backtest result is only trustworthy when all of the following are true:

1. Data source and fingerprint are recorded.
2. Strategy config is fully serialized and versioned.
3. Costs and fill rules are explicit.
4. No known leakage path exists.
5. The run is reproducible.
6. The strategy is evaluated on out-of-sample data.
7. Metrics are not cherry-picked.
8. Rejection reasons are preserved for failed or weak candidates.

Any result lacking these conditions should be labeled exploratory only.

---

## 23. Open design decisions, choose conservatively

If unresolved during implementation, prefer:
1. lower leakage risk,
2. more conservative fills,
3. fewer assumptions,
4. simpler testable design,
5. explicit rejection over silent tolerance.

Specific defaults:
- next-bar open entry
- pessimistic same-bar stop/target resolution
- conservative cost assumptions
- stable config schemas
- strategy selection based on validation, not final test

---

## 24. First end-to-end target

The first meaningful demonstration should be:

- one canonical dataset for EURUSD 1H
- a small fixture dataset and a larger sample dataset
- 6 to 10 features
- 3 strategy templates
- backtest engine with costs and ATR-based sizing
- single-indicator sweep over the sample dataset
- train / validation / test split
- one leaderboard report
- full automated test suite passing

This is the minimum viable research lab.

---

## 25. Final instruction to the coding agent

Implement the system in thin vertical slices:
- data,
- features,
- rules,
- execution,
- evaluation,
- validation,
- reporting.

After each slice:
- add tests,
- run commands,
- verify reproducibility,
- preserve conservative assumptions,
- avoid broad speculative abstractions unless they remove clear duplication.

The lab should be easy to trust before it is easy to extend.
