# FXLab

`fxlab` is a deterministic FX systematic strategy lab focused on correctness,
reproducibility, and anti-bias controls.

The repository now includes:
- internal Dukascopy provider contracts
- canonical normalization and dataset fingerprinting
- feature engine foundations with `SMA`, `EMA`, `RSI`, and `ATR`
- config-driven strategy DSL
- conservative execution and risk sizing
- portfolio/accounting and metrics
- run registry and reporting
- single-pair and multi-pair mocked vertical slices

## Repo guides

- `AGENTS.md`
- `PLANS.md`
- `TASKS.md`
- `TASKS_EXECUTION_ORDER.md`
- `REPO_STRUCTURE.md`
- `docs/architecture.md`
- `docs/troubleshooting.md`

## Setup

Use the project virtual environment, then run:

```bash
make setup
```

If dependencies were already installed into `.venv`, use the environment-local tools:

```bash
.venv\Scripts\python.exe -m ruff check .
.venv\Scripts\python.exe -m pytest
```

## Stable commands

- `make setup`
- `make lint`
- `make typecheck`
- `make test`
- `make test-unit`
- `make test-integration`
- `make smoke`
- `make example-run`

## Example run

The current example config is:

- `configs/experiments/vertical_slice_demo.yaml`

The current end-to-end integration path is exercised by:

- `tests/integration/test_vertical_slice_pipeline.py`
- `tests/integration/test_multi_pair_vertical_slice.py`

## Current constraints

- historical download wiring is still mocked through injected fetchers in tests
- execution is intentionally narrow and conservative
- reporting is JSON/data oriented rather than HTML heavy
- combination sweeps and performance tuning are still pending
