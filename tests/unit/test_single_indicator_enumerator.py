"""Single-indicator sweep enumeration tests."""

from fxlab.experiments.single_indicator import enumerate_single_indicator_candidates


def test_enumerate_single_indicator_candidates_is_deterministic() -> None:
    candidates = enumerate_single_indicator_candidates(
        {
            "rsi": {"length": (14, 7)},
            "ema": {"length": (50, 20)},
        }
    )

    assert [candidate.candidate_id for candidate in candidates] == [
        "ema__length_50",
        "ema__length_20",
        "rsi__length_14",
        "rsi__length_7",
    ]


def test_enumerator_supports_multiple_params() -> None:
    candidates = enumerate_single_indicator_candidates(
        {
            "atr": {"length": (14,), "multiple": (1.0, 2.0)},
        }
    )

    assert [candidate.candidate_id for candidate in candidates] == [
        "atr__length_14_multiple_1.0",
        "atr__length_14_multiple_2.0",
    ]
