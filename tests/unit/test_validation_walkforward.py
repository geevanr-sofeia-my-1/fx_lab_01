"""Walk-forward schedule tests."""

from fxlab.validation.walkforward import build_walkforward_schedule


def test_build_walkforward_schedule_produces_expected_windows() -> None:
    schedule = build_walkforward_schedule(
        total_rows=20,
        train_size=10,
        validation_size=5,
        step_size=3,
    )

    assert schedule[0].train_start == 0
    assert schedule[0].validation_start == 10
    assert schedule[1].train_start == 3
    assert schedule[1].validation_end == 18
