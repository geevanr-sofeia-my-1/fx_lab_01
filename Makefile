PYTHON ?= python

.PHONY: setup lint typecheck test test-unit test-integration smoke example-run

setup:
	$(PYTHON) -m pip install -e ".[dev]"

lint:
	$(PYTHON) -m ruff check .

typecheck:
	$(PYTHON) -m mypy src

test:
	$(PYTHON) -m pytest

test-unit:
	$(PYTHON) -m pytest tests/unit

test-integration:
	$(PYTHON) -m pytest tests/integration

smoke:
	$(PYTHON) -m pytest tests/unit/test_import_smoke.py tests/unit/test_config_loader.py

example-run:
	$(PYTHON) main.py --config configs/app/bootstrap.yaml
