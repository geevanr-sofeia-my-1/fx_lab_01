"""Feature alignment tests."""

import pytest

from fxlab.features.alignment import rolling_mean, shift_values


def test_shift_values_adds_leading_nones() -> None:
    assert shift_values((1.0, 2.0, 3.0), periods=1) == (None, 1.0, 2.0)


def test_shift_values_rejects_negative_periods() -> None:
    with pytest.raises(ValueError):
        shift_values((1.0, 2.0), periods=-1)


def test_rolling_mean_includes_warmup_nones() -> None:
    assert rolling_mean((1.0, 2.0, 3.0, 4.0), window=3) == (None, None, 2.0, 3.0)
