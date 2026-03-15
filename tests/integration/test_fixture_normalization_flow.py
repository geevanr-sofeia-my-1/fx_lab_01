"""Fixture-backed normalization integration test."""

from fxlab.data.normalize.canonical import normalize_raw_bars  # noqa: I001
from tests.fixtures.canonical_fixtures import session_boundary_rows


def test_fixture_rows_normalize_into_canonical_bars() -> None:
    bars = normalize_raw_bars(
        session_boundary_rows(),
        pair="EURUSD",
        timeframe="1H",
        source="fixture",
        provider="dukascopy",
        price_basis="mid",
    )

    assert len(bars) == 3
    assert bars[0].session_asia is True
    assert bars[1].session_london is True
    assert bars[2].session_newyork is True
