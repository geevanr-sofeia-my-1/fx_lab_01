# Troubleshooting

## Ruff says "No module named ruff"

This usually means the active interpreter is not the repo virtual environment.

Use:

```bash
.venv\Scripts\python.exe -m ruff check .
```

## Mypy says "No module named mypy"

The current environment may not have `mypy` installed yet even if runtime and test tools exist.
Install dev dependencies into the repo venv or run `make setup`.

## Ruff prints `Access is denied` warnings on Windows

The current environment may emit Windows file-access warnings after `ruff` completes.
If `ruff` ends with `All checks passed!`, treat lint as passing unless the exit code is non-zero.

## Tests pass but provider downloads are mocked

That is expected in the current state. The vertical slice uses injected fetchers and deterministic
CSV artifacts to exercise the architecture without live network dependency.

## Where to start reading the code

Start with:

1. `src/fxlab/experiments/pipeline.py`
2. `src/fxlab/data/normalize/`
3. `src/fxlab/features/`
4. `src/fxlab/strategy/`
5. `src/fxlab/execution/`
