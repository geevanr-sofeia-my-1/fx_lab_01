"""Risk sizing tests."""

import pytest

from fxlab.risk.sizing import atr_based_size, fixed_fractional_size, fixed_lot_size


def test_fixed_lot_size_respects_rounding() -> None:
    assert fixed_lot_size(lot_size=0.137, min_lot=0.01, lot_step=0.01) == 0.13


def test_fixed_fractional_size_is_deterministic() -> None:
    size = fixed_fractional_size(
        equity=500.0,
        risk_fraction=0.01,
        stop_distance=2.0,
        min_lot=0.01,
        lot_step=0.01,
    )
    assert size == 2.5


def test_atr_based_size_uses_atr_stop_distance() -> None:
    size = atr_based_size(
        equity=500.0,
        risk_fraction=0.01,
        atr_value=1.0,
        atr_multiple=2.0,
        min_lot=0.01,
        lot_step=0.01,
    )
    assert size == 2.5


def test_fractional_size_rejects_infeasible_small_position() -> None:
    with pytest.raises(ValueError):
        fixed_fractional_size(
            equity=10.0,
            risk_fraction=0.001,
            stop_distance=100.0,
            min_lot=0.01,
            lot_step=0.01,
        )
