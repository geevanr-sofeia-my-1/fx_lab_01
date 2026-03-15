# TASKS_EXECUTION_ORDER.md

## Purpose

This file converts `TASKS.md` into smaller execution tickets for the coding agent.

Each ticket should be implementable in a narrow, reviewable slice. The goal is to reduce architectural drift, lower bug surface area, and force correctness before scale.

Complete tickets in order unless a later ticket explicitly says it can run in parallel.

---

## Global rules

1. Read `AGENTS.md`, `PLANS.md`, and `TASKS.md` before starting.
2. Do not skip ahead to strategy sweeps before the data and execution layers are proven.
3. Every ticket must end with:
   - code complete
   - tests passing
   - docs updated if interfaces changed
   - no TODO placeholders for critical logic
4. No silent assumptions:
   - timestamp timezone
   - price basis
   - fill ordering
   - risk sizing
   - missing data policy
5. Prefer conservative assumptions when uncertain.
6. Do not optimize performance before reference correctness exists.

---

# Phase 0: Repository foundation

## Current Resume Point

The repository has progressed far beyond the early tickets in this file.

Completed enough to count as implemented foundation:

- Phase 0 through Phase 19 core path, including:
  - repository bootstrap
  - schemas and domain types
  - provider contracts and raw manifests
  - canonical normalization and quality/fingerprint logic
  - fixtures and session labeling
  - feature engine and initial indicators
  - strategy DSL
  - risk sizing
  - execution
  - portfolio/accounting
  - metrics
  - registry
  - single-indicator enumeration
  - validation helpers
  - anti-bias regressions
  - reporting helpers
  - single-pair vertical slice
  - multi-pair vertical slice

Also completed after the critical path:

- controlled combination generation (`Task 16` / Phase 20 foundation)
- documentation/examples (`Task 23` / Phase 22 foundation)

Current validation status:

- `ruff` passes
- `pytest` passes
- current passing test count: 112

Primary next work item for a new agent:

- Phase 21 / `Task 22`: profile the reference pipeline and optimize only with parity checks

Important implementation note:

- The end-to-end pipeline is currently exercised with deterministic injected fetchers rather than live `dukascopy-python` network access.
- Any future live-provider work must preserve the existing conservative assumptions and regression behavior.

## Ticket 00.1: Create repository skeleton

### Scope
Create the basic project structure.

### Deliverables
- `src/fxlab/`
- `tests/unit/`
- `tests/integration/`
- `tests/regression/`
- `tests/fixtures/`
- `docs/`
- `artifacts/`
- `configs/`

### Done when
- package imports work
- pytest discovers tests
- directories are created deterministically

### Tests
- import smoke test
- directory creation smoke test

---

## Ticket 00.2: Add project tooling

### Scope
Set up Python packaging and engineering tools.

### Deliverables
- `pyproject.toml`
- lint config
- formatter config
- type checker config
- `Makefile`
- minimal dependency groups:
  - core
  - dev
  - test

### Done when
- lint command works
- type check command works
- test command works

### Tests
- config parse smoke tests

---

## Ticket 00.3: Add config loader and logging

### Scope
Create reusable config loading and logging primitives.

### Deliverables
- config loader
- logging setup
- path utilities
- artifact root management

### Done when
- config file loads into typed structure
- logger can be instantiated from config

### Tests
- config loader smoke test
- artifact path creation test
- logging initialization test

---

# Phase 1: Contracts and schemas

## Ticket 01.1: Define base enums and value objects

### Scope
Create foundational types used across the lab.

### Deliverables
- timeframe enum
- pair enum
- price basis enum
- entry timing enum
- position mode enum
- bar schema value object

### Done when
- invalid values fail loudly
- enums are serializable

### Tests
- enum validation tests
- serialization roundtrip tests

---

## Ticket 01.2: Define config schemas

### Scope
Create typed models for the lab’s major config surfaces.

### Deliverables
- dataset request config
- canonical dataset manifest schema
- feature job config
- strategy config
- execution config
- risk config
- experiment config
- validation config

### Done when
- all major config models validate
- missing required fields raise errors

### Tests
- valid config tests
- invalid config rejection tests
- version field tests where relevant

---

## Ticket 01.3: Define run metadata and fingerprint schemas

### Scope
Create reproducibility metadata structures.

### Deliverables
- dataset fingerprint schema
- run metadata schema
- config hash support
- code version capture schema

### Done when
- metadata can be serialized deterministically
- schemas are reusable across modules

### Tests
- metadata serialization tests
- deterministic hashing tests

---

# Phase 2: Data provider layer

## Ticket 02.1: Create provider abstraction

### Scope
Define the internal interface for historical data providers.

### Deliverables
- `HistoricalDataProvider` interface
- provider request object
- provider response object
- provider exception hierarchy

### Done when
- downstream code depends only on interface, not vendor library

### Tests
- interface contract tests with mock provider

---

## Ticket 02.2: Implement Dukascopy instrument and timeframe mapping

### Scope
Map internal symbols and timeframes to Dukascopy-compatible requests.

### Deliverables
- pair mapping
- timeframe mapping
- validation rules

### Done when
- unsupported mappings fail clearly
- mappings are deterministic

### Tests
- mapping tests for all initial 6 pairs
- timeframe mapping tests
- invalid mapping tests

---

## Ticket 02.3: Implement Dukascopy download adapter

### Scope
Build the actual provider adapter using `dukascopy-python`.

### Deliverables
- `DukascopyProvider`
- request execution
- chunked range download support
- adapter-level logging
- raw artifact save path strategy

### Done when
- downloads can be requested through internal interface only
- direct vendor calls are isolated to adapter module

### Tests
- mocked provider request test
- chunked download flow test
- failure path test

---

## Ticket 02.4: Add raw download manifest and checksum support

### Scope
Persist enough metadata to reproduce and audit every download.

### Deliverables
- raw manifest writer
- content hash or checksum generation
- source metadata capture:
  - provider name
  - pair
  - timeframe
  - start
  - end
  - request parameters
  - price basis if known

### Done when
- every download writes a manifest
- checksums are deterministic

### Tests
- manifest creation test
- checksum determinism test

---

# Phase 3: Canonical dataset creation

## Ticket 03.1: Define canonical bar format

### Scope
Lock the schema for normalized bar data.

### Deliverables
- canonical column set
- required dtypes
- timestamp rules
- sorting rules
- uniqueness key definition

### Done when
- schema is documented and machine-validated

### Tests
- schema validation tests

---

## Ticket 03.2: Build raw-to-canonical normalization

### Scope
Convert provider output into canonical bars.

### Deliverables
- UTC normalization
- column normalization
- sorting
- duplicate detection
- basic OHLC sanity checks

### Done when
- normalized bars conform to canonical schema
- invalid rows are surfaced, not silently hidden

### Tests
- UTC normalization tests
- duplicate handling tests
- OHLC sanity tests

---

## Ticket 03.3: Add resampling engine

### Scope
Support deterministic timeframe aggregation where needed.

### Deliverables
- resampling logic
- aggregation rules for OHLC
- metadata propagation
- reproducibility safeguards

### Done when
- repeated runs produce identical resampled output

### Tests
- resample correctness tests
- deterministic output tests

---

## Ticket 03.4: Add dataset fingerprinting and quality reports

### Scope
Make canonical datasets auditable.

### Deliverables
- dataset fingerprint
- row counts
- start and end range
- duplicate count
- gap count
- null summary
- quality report file

### Done when
- every canonical dataset can be fingerprinted and audited

### Tests
- fingerprint determinism tests
- quality report smoke test

---

# Phase 4: Fixture system

## Ticket 04.1: Create tiny canonical fixture datasets

### Scope
Build small deterministic datasets for unit and regression testing.

### Deliverables
Fixtures for:
- clean bars
- duplicate timestamps
- missing intervals
- flat bars
- stop and target same-bar ambiguity
- session boundary cases

### Done when
- fixtures are easy to inspect and stable across runs

### Tests
- fixture integrity tests
- fixture loader tests

---

# Phase 5: Session and price-basis semantics

## Ticket 05.1: Implement session labeling

### Scope
Add deterministic session tagging.

### Deliverables
- Asia session label
- London session label
- New York session label
- overlap support if applicable

### Done when
- session labels are deterministic for UTC bars

### Tests
- session boundary tests
- overlap tests

---

## Ticket 05.2: Implement explicit price-basis propagation

### Scope
Carry `price_basis` through data and later execution layers.

### Deliverables
- price basis metadata field
- propagation logic through manifests and canonical data
- validation guards for unknown basis

### Done when
- no dataset can be used without explicit price basis

### Tests
- metadata propagation tests
- missing basis rejection tests

---

# Phase 6: Feature engine foundation

## Ticket 06.1: Build feature registry and feature interface

### Scope
Create the contract for all computed features.

### Deliverables
- feature base class or protocol
- feature registry
- parameter signature handling
- output column naming standard

### Done when
- features can be registered and called consistently

### Tests
- registry tests
- naming convention tests

---

## Ticket 06.2: Build feature job runner

### Scope
Execute feature computations over canonical datasets.

### Deliverables
- feature job runner
- artifact writer
- feature manifest
- feature fingerprint

### Done when
- feature jobs can be run from config
- outputs are reproducible

### Tests
- feature job smoke test
- fingerprint determinism test

---

## Ticket 06.3: Add alignment and anti-leakage helpers

### Scope
Prevent accidental future leakage in rolling features.

### Deliverables
- lag helper
- shift helper
- decision-time alignment utilities
- validation guards for future-index access

### Done when
- feature alignment is explicit and testable

### Tests
- rolling alignment tests
- lookahead regression tests

---

# Phase 7: Initial feature set

## Ticket 07.1: Implement moving average features

### Scope
Add simple trend features.

### Deliverables
- SMA
- EMA

### Done when
- outputs match trusted references within tolerance

### Tests
- parity tests on fixture data
- warmup NaN behavior tests

---

## Ticket 07.2: Implement momentum and oscillator features

### Scope
Add common momentum indicators.

### Deliverables
- RSI
- Stochastic
- MACD

### Done when
- outputs are stable and parameterized

### Tests
- reference parity tests
- parameterized tests

---

## Ticket 07.3: Implement volatility and channel features

### Scope
Add volatility and structure features.

### Deliverables
- ATR
- Bollinger Bands
- Donchian channels
- rolling volatility

### Done when
- outputs are documented and reproducible

### Tests
- parity tests
- edge-case tests

---

## Ticket 07.4: Implement regime helper features

### Scope
Add features useful for filters and analysis.

### Deliverables
- range compression
- expansion flags
- session features
- simple trend slope or structure helpers

### Done when
- regime features are available from the same feature engine

### Tests
- fixture-based regime tests

---

# Phase 8: Candlestick features

## Ticket 08.1: Implement candlestick pattern framework

### Scope
Create a deterministic framework for bar-pattern labeling.

### Deliverables
- pattern interface
- naming rules
- threshold support where needed

### Done when
- patterns are explicit and config-driven

### Tests
- framework smoke tests

---

## Ticket 08.2: Implement first candlestick set

### Scope
Add the initial pattern library.

### Deliverables
- doji
- engulfing
- hammer
- shooting star
- inside bar
- outside bar

### Done when
- each pattern has explicit rule logic

### Tests
- pattern fixture tests
- edge-case classification tests
- no-lookahead tests

---

# Phase 9: Strategy grammar

## Ticket 09.1: Define strategy DSL schema

### Scope
Represent strategies in config, not hand-coded scripts.

### Deliverables
- strategy root schema
- setup block
- trigger block
- filter block
- exit block
- sizing block

### Done when
- a strategy can be fully declared from config

### Tests
- valid strategy config tests
- invalid strategy rejection tests

---

## Ticket 09.2: Implement signal primitives

### Scope
Create reusable signal conditions.

### Deliverables
- cross above
- cross below
- threshold above
- threshold below
- band touch
- breakout

### Done when
- primitives behave deterministically on aligned data

### Tests
- crossover tests
- threshold tests
- breakout tests

---

## Ticket 09.3: Implement signal composition

### Scope
Support compound logic.

### Deliverables
- AND
- OR
- NOT
- optional sequential gating

### Done when
- compound rules can be evaluated from config

### Tests
- boolean composition tests
- gating order tests

---

# Phase 10: Risk and money management

## Ticket 10.1: Implement fixed lot sizing

### Scope
Create baseline position sizing.

### Deliverables
- fixed lot model
- rounding rules

### Done when
- same inputs always produce same size

### Tests
- fixed lot tests

---

## Ticket 10.2: Implement fixed fractional risk sizing

### Scope
Size positions by account risk fraction.

### Deliverables
- fractional sizing model
- account equity input support
- cap logic

### Done when
- position size obeys risk fraction rules

### Tests
- fractional sizing tests
- cap tests

---

## Ticket 10.3: Implement ATR-based stop sizing

### Scope
Support volatility-based stop and size calculation.

### Deliverables
- ATR stop distance
- size from stop distance and account risk
- unit rounding

### Done when
- ATR stop sizing is deterministic and isolated from entry logic

### Tests
- ATR sizing tests
- edge-case low-volatility tests

---

## Ticket 10.4: Implement account protection rules

### Scope
Add optional risk brakes.

### Deliverables
- max daily loss rule
- drawdown brake
- cooldown logic

### Done when
- protection rules can block new entries when triggered

### Tests
- drawdown brake tests
- cooldown tests

---

# Phase 11: Execution engine

## Ticket 11.1: Define order and fill models

### Scope
Create internal execution state objects.

### Deliverables
- order model
- position model
- fill event model
- trade model

### Done when
- execution engine can operate on explicit objects

### Tests
- model construction tests

---

## Ticket 11.2: Implement next-bar-open entry logic

### Scope
Create the default conservative entry model.

### Deliverables
- signal-to-order translation
- next-bar-open fill logic

### Done when
- same-bar fantasy entry is not used by default

### Tests
- next-bar entry tests
- no same-bar entry regression test

---

## Ticket 11.3: Implement stop-loss and take-profit handling

### Scope
Support exits under explicit bar-based assumptions.

### Deliverables
- stop logic
- target logic
- tie-break policy when both touched in same bar
- documented conservative rule

### Done when
- ambiguous same-bar cases are handled consistently

### Tests
- stop tests
- target tests
- tie-break tests

---

## Ticket 11.4: Implement cost model

### Scope
Add realistic frictions.

### Deliverables
- fixed spread model
- slippage model
- interaction with price basis

### Done when
- costs are applied consistently and visibly

### Tests
- spread tests
- slippage tests
- price-basis interaction tests

---

# Phase 12: Portfolio accounting

## Ticket 12.1: Implement account state engine

### Scope
Track cash, equity, and open exposure.

### Deliverables
- cash tracking
- equity tracking
- open position list
- realized and unrealized PnL logic

### Done when
- account state is coherent across time

### Tests
- cash update tests
- equity curve tests

---

## Ticket 12.2: Implement portfolio constraints

### Scope
Add portfolio-wide controls.

### Deliverables
- max open trades
- per-pair exposure cap
- one-position-per-pair option if needed

### Done when
- constraints block invalid entries consistently

### Tests
- max open trades tests
- per-pair cap tests

---

# Phase 13: Metrics and evaluation

## Ticket 13.1: Implement trade-level metrics

### Scope
Compute basic trade statistics.

### Deliverables
- win rate
- expectancy
- average trade
- profit factor

### Done when
- metrics can be computed from trade log alone

### Tests
- trade metric fixture tests

---

## Ticket 13.2: Implement equity and risk metrics

### Scope
Compute portfolio-level evaluation metrics.

### Deliverables
- return series
- drawdown series
- max drawdown
- Sharpe-like metrics
- CAGR where appropriate

### Done when
- metrics are documented and deterministic

### Tests
- drawdown tests
- return series tests
- metric correctness tests

---

## Ticket 13.3: Implement grouped breakdown metrics

### Scope
Support deeper analysis.

### Deliverables
Metrics by:
- pair
- year
- regime
- split

### Done when
- grouped stats match full-run decomposition rules

### Tests
- grouped aggregation tests

---

# Phase 14: Experiment tracking

## Ticket 14.1: Implement run registry

### Scope
Persist experiment metadata.

### Deliverables
- registry database
- run insertion
- run status updates
- artifact path tracking

### Done when
- every experiment is recorded

### Tests
- run registration tests
- failed run status tests

---

## Ticket 14.2: Add duplicate-run detection

### Scope
Prevent silent duplication and support reproducibility.

### Deliverables
- config hash
- dataset fingerprint storage
- dedupe check

### Done when
- identical runs can be identified

### Tests
- duplicate detection tests
- metadata completeness tests

---

# Phase 15: Single-indicator sweep

## Ticket 15.1: Build single-indicator enumerator

### Scope
Generate controlled strategy candidates from one indicator at a time.

### Deliverables
- enumerator logic
- parameter grid support
- standardized execution and risk hooks

### Done when
- indicator candidates are generated from config

### Tests
- enumeration tests
- bounds tests

---

## Ticket 15.2: Execute and store single-indicator runs

### Scope
Run the first systematic experiment batch.

### Deliverables
- batch runner
- result persistence
- artifact writing

### Done when
- runs can be executed reproducibly and stored

### Tests
- deterministic rerun test
- artifact creation test

---

## Ticket 15.3: Build single-indicator leaderboard

### Scope
Summarize the first research stage.

### Deliverables
- leaderboard table
- warning flags for low trade count
- ranking by composite score, not return only

### Done when
- results are inspectable and traceable

### Tests
- leaderboard tests
- warning flag tests

---

# Phase 16: Validation framework

## Ticket 16.1: Implement split logic

### Scope
Separate training, selection, and final evaluation windows.

### Deliverables
- in-sample split
- validation split
- final test split
- split manifest

### Done when
- final test segment is isolated

### Tests
- split boundary tests
- leakage prevention tests

---

## Ticket 16.2: Implement walk-forward engine

### Scope
Support rolling validation.

### Deliverables
- walk-forward schedule
- repeated train-validate loop
- output aggregation

### Done when
- walk-forward results are reproducible

### Tests
- walk-forward correctness tests

---

## Ticket 16.3: Implement robustness checks

### Scope
Add robustness analysis around selected strategies.

### Deliverables
- minimum trade count rule
- sensitivity analysis
- cost stress tests
- Monte Carlo with fixed seed

### Done when
- fragile strategies are visibly penalized or flagged

### Tests
- sensitivity smoke tests
- Monte Carlo determinism tests
- cost stress tests

---

# Phase 17: Anti-bias regression suite

## Ticket 17.1: Add lookahead regression tests

### Scope
Create deliberate failure traps for future leakage.

### Deliverables
Regression tests for:
- unshifted rolling feature
- future bar access
- future volatility use

### Done when
- regression suite fails if leakage is reintroduced

### Tests
- one regression test per failure mode

---

## Ticket 17.2: Add execution bias regression tests

### Scope
Protect execution realism.

### Deliverables
Regression tests for:
- same-bar fantasy entry
- same-bar stop and target optimism
- cost omission

### Done when
- optimistic fill assumptions are caught automatically

### Tests
- one regression test per failure mode

---

## Ticket 17.3: Add selection bias regression tests

### Scope
Protect the research process.

### Deliverables
Regression tests for:
- using final test results in ranking
- mixing out-of-sample metrics into candidate selection
- mismatched dataset fingerprint use

### Done when
- selection leakage is caught by CI

### Tests
- one regression test per failure mode

---

# Phase 18: Reporting

## Ticket 18.1: Build run summary report

### Scope
Generate concise run-level output.

### Deliverables
- run summary
- metrics summary
- config snapshot
- dataset fingerprint reference

### Done when
- every completed run has a readable summary

### Tests
- report generation smoke test

---

## Ticket 18.2: Build validation report

### Scope
Summarize robustness results.

### Deliverables
- split performance summary
- walk-forward summary
- sensitivity summary
- warnings

### Done when
- validation outcomes are clearly separated from raw backtest output

### Tests
- validation report smoke test

---

## Ticket 18.3: Build leaderboard report outputs

### Scope
Generate ranked research views.

### Deliverables
- leaderboard export
- by-pair breakdown
- by-year breakdown
- flagged unstable strategies

### Done when
- leaderboard rows are traceable to exact run metadata

### Tests
- leaderboard schema tests
- flagged strategy tests

---

# Phase 19: End-to-end slices

## Ticket 19.1: Single-pair vertical slice

### Scope
Run one full workflow from download to report.

### Suggested slice
- pair: EURUSD
- timeframe: 1H
- limited fixed time range
- simple strategy:
  - EMA trend filter
  - RSI trigger
  - ATR stop sizing

### Deliverables
- config files
- pipeline command
- output artifacts
- run registry entry
- report

### Done when
- same inputs reproduce same outputs

### Tests
- end-to-end integration test
- deterministic rerun test

---

## Ticket 19.2: Multi-pair vertical slice

### Scope
Extend the full workflow to initial 6 pairs.

### Deliverables
- multi-pair config
- aggregate reporting
- pair-level metrics

### Done when
- portfolio accounting and reporting work across multiple pairs

### Tests
- multi-pair integration test
- aggregate consistency tests

---

# Phase 20: Controlled combination search

## Ticket 20.1: Build 2-indicator combination generator

### Scope
Expand search space carefully.

### Deliverables
- role-aware combination generation
- redundancy filters
- config controls for max combinations

### Done when
- combinations are meaningful, bounded, and reproducible

### Tests
- combination generation tests
- redundancy filter tests

---

## Ticket 20.2: Build 3-indicator combination generator

### Scope
Add limited triple combinations only after 2-indicator framework is stable.

### Deliverables
- role-aware triple generation
- search-space constraints

### Done when
- triple search remains controlled, not brute-force chaos

### Tests
- triple generation tests
- search-space bound tests

---

## Ticket 20.3: Execute and report selected combinations

### Scope
Run narrowed combination experiments.

### Deliverables
- batch execution
- stored results
- leaderboard integration
- robustness flags

### Done when
- selected combinations can be compared fairly against single-indicator baselines

### Tests
- combination run smoke test
- deterministic rerun test

---

# Phase 21: Performance work

## Ticket 21.1: Profile reference pipeline

### Scope
Measure before optimizing.

### Deliverables
- profiling report
- bottleneck list
- candidate optimization plan

### Done when
- top runtime bottlenecks are identified with evidence

### Tests
- profiling command smoke test

---

## Ticket 21.2: Optimize safe hotspots

### Scope
Improve runtime without changing outputs.

### Deliverables
Possible targets:
- caching
- vectorization
- selective parallelism
- artifact reuse

### Done when
- optimized outputs match reference outputs exactly or within documented tolerances

### Tests
- parity tests
- cache correctness tests

---

# Phase 22: Documentation

## Ticket 22.1: Update README and architecture docs

### Scope
Make the system usable by a human researcher.

### Deliverables
- local setup
- architecture overview
- pipeline overview
- reproducibility notes

### Done when
- docs match actual commands and config names

### Tests
- docs command smoke tests where feasible

---

## Ticket 22.2: Add example configs and usage walkthroughs

### Scope
Provide working examples for the main research flows.

### Deliverables
- dataset download config
- feature job config
- simple strategy config
- sweep config
- validation config

### Done when
- examples validate against current schema

### Tests
- example config validation tests

---

# Critical path

The minimum path to a trustworthy v1 vertical slice is:

1. 00.1
2. 00.2
3. 00.3
4. 01.1
5. 01.2
6. 01.3
7. 02.1
8. 02.2
9. 02.3
10. 02.4
11. 03.1
12. 03.2
13. 03.3
14. 03.4
15. 04.1
16. 05.1
17. 05.2
18. 06.1
19. 06.2
20. 06.3
21. 07.1
22. 07.2
23. 07.3
24. 08.1
25. 08.2
26. 09.1
27. 09.2
28. 09.3
29. 10.1
30. 10.2
31. 10.3
32. 11.1
33. 11.2
34. 11.3
35. 11.4
36. 12.1
37. 12.2
38. 13.1
39. 13.2
40. 14.1
41. 14.2
42. 15.1
43. 15.2
44. 15.3
45. 16.1
46. 16.2
47. 16.3
48. 17.1
49. 17.2
50. 17.3
51. 18.1
52. 18.2
53. 18.3
54. 19.1

Only after that should the agent proceed to:
- 19.2
- 20.1
- 20.2
- 20.3
- 21.1
- 21.2
- 22.1
- 22.2

---

# Stop conditions

The agent must stop and surface the issue if any of the following occur:

1. Dukascopy adapter cannot produce deterministic normalized output.
2. Price basis is ambiguous or missing.
3. Feature alignment cannot be proven leak-free.
4. Execution tie-break rules are not explicit.
5. Final test segment is being used during model selection.
6. Results differ across reruns with identical config and dataset fingerprint.
7. Cost assumptions are bypassed or omitted.
8. Anti-bias regression tests fail.

---

# Definition of ready for broad sweeps

Do not launch large indicator or combination sweeps until all of the following are true:

1. Single-pair vertical slice passes.
2. Run registry is working.
3. Anti-bias regression suite is green.
4. Metrics and reports are traceable.
5. Cost model is active.
6. Strategy configs are fully declarative.
7. Validation split logic is enforced.
8. Deterministic rerun tests pass.

---

# Definition of ready for Codex autonomous execution

The repo is ready for broader agentic coding once:

1. `AGENTS.md`, `PLANS.md`, `TASKS.md`, and this file are present.
2. Core interfaces are stable.
3. Acceptance criteria are explicit per ticket.
4. Test commands are stable.
5. Artifact paths and run metadata conventions are fixed.
6. The agent can pick the next unfinished ticket and execute it without guessing architecture.
