"""Deterministic position sizing models."""

from __future__ import annotations

import math


def _round_down(value: float, step: float) -> float:
    """Round down to the nearest allowed sizing step."""
    if step <= 0:
        raise ValueError("step must be positive")
    return math.floor(value / step) * step


def fixed_lot_size(*, lot_size: float, min_lot: float = 0.01, lot_step: float = 0.01) -> float:
    """Return a fixed lot size subject to broker-like granularity constraints."""
    if lot_size <= 0:
        raise ValueError("lot_size must be positive")
    if lot_size < min_lot:
        raise ValueError("lot_size is below minimum executable size")
    rounded = _round_down(lot_size, lot_step)
    if rounded < min_lot:
        raise ValueError("rounded lot_size is below minimum executable size")
    return rounded


def fixed_fractional_size(
    *,
    equity: float,
    risk_fraction: float,
    stop_distance: float,
    min_lot: float = 0.01,
    lot_step: float = 0.01,
) -> float:
    """Size a position from account equity, risk fraction, and stop distance."""
    if equity <= 0:
        raise ValueError("equity must be positive")
    if not 0 < risk_fraction <= 1:
        raise ValueError("risk_fraction must be in (0, 1]")
    if stop_distance <= 0:
        raise ValueError("stop_distance must be positive")

    risk_amount = equity * risk_fraction
    raw_size = risk_amount / stop_distance
    rounded = _round_down(raw_size, lot_step)
    if rounded < min_lot:
        raise ValueError("calculated size is below minimum executable size")
    return rounded


def atr_based_size(
    *,
    equity: float,
    risk_fraction: float,
    atr_value: float,
    atr_multiple: float,
    min_lot: float = 0.01,
    lot_step: float = 0.01,
) -> float:
    """Size a position from ATR-derived stop distance and account risk."""
    if atr_value <= 0:
        raise ValueError("atr_value must be positive")
    if atr_multiple <= 0:
        raise ValueError("atr_multiple must be positive")
    stop_distance = atr_value * atr_multiple
    return fixed_fractional_size(
        equity=equity,
        risk_fraction=risk_fraction,
        stop_distance=stop_distance,
        min_lot=min_lot,
        lot_step=lot_step,
    )
