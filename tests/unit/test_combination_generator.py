"""Combination generator tests."""

from fxlab.experiments.combinations import (
    IndicatorSpec,
    generate_three_indicator_combinations,
    generate_two_indicator_combinations,
)


def _indicators() -> tuple[IndicatorSpec, ...]:
    return (
        IndicatorSpec(candidate_id="ema_20", role="trend"),
        IndicatorSpec(candidate_id="rsi_14", role="trigger"),
        IndicatorSpec(candidate_id="atr_14", role="risk"),
        IndicatorSpec(candidate_id="ema_50", role="trend"),
    )


def test_generate_two_indicator_combinations_filters_same_role_pairs() -> None:
    combinations = generate_two_indicator_combinations(_indicators())

    ids = [item.candidate_id for item in combinations]
    assert "ema_20__ema_50" not in ids
    assert "ema_20__rsi_14" in ids
    assert "atr_14__rsi_14" in ids


def test_generate_three_indicator_combinations_require_distinct_roles() -> None:
    combinations = generate_three_indicator_combinations(_indicators())

    ids = [item.candidate_id for item in combinations]
    assert ids == [
        "atr_14__ema_20__rsi_14",
        "atr_14__ema_50__rsi_14",
    ]
