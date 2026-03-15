"""Fixture builder tests."""

from tests.fixtures.canonical_fixtures import (
    clean_hourly_rows,
    duplicate_timestamp_rows,
    same_bar_ambiguity_rows,
    session_boundary_rows,
)


def test_fixture_builders_return_expected_shapes() -> None:
    assert len(clean_hourly_rows()) == 4
    assert len(duplicate_timestamp_rows()) == 5
    assert len(same_bar_ambiguity_rows()) == 2
    assert len(session_boundary_rows()) == 3
