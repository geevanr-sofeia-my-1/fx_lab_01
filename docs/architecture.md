# Architecture

## Implemented layers

The current repository has working foundations for:

1. Data provider contracts and raw download manifests
2. Canonical normalization, session labeling, and dataset fingerprinting
3. Feature registry, alignment helpers, and core indicators
4. Strategy DSL with primitive predicates and boolean composition
5. Conservative execution and sizing
6. Portfolio/accounting and metrics
7. Registry, reporting, validation helpers, and anti-bias regressions
8. Single-pair and multi-pair vertical slices

## Current vertical slice

The current end-to-end path is centered on:

- `src/fxlab/experiments/pipeline.py`
- `src/fxlab/experiments/multi_pair.py`

It performs:

1. provider request and raw artifact write
2. raw manifest generation
3. canonical normalization
4. feature computation
5. strategy evaluation
6. risk field attachment
7. conservative execution
8. portfolio update
9. metrics and report summary generation
10. registry persistence

## Important conservative assumptions

- signals are shifted before entry by default
- entries occur at next bar open
- same-bar stop/target ambiguity is resolved pessimistically
- low trade count is penalized in leaderboard scoring
- split windows are explicit and non-overlapping

## Key paths

- package root: `src/fxlab/`
- examples: `configs/experiments/`
- tests: `tests/unit/`, `tests/integration/`, `tests/regression/`
- artifacts: `artifacts/`
