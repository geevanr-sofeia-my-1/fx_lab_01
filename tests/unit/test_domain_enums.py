"""Enum contract tests."""

from pydantic import TypeAdapter, ValidationError

from fxlab.domain.enums import EntryTiming, Pair, PositionMode, PriceBasis, Timeframe


def test_timeframe_enum_validates() -> None:
    adapter = TypeAdapter(Timeframe)
    assert adapter.validate_python("1H") == Timeframe.H1


def test_pair_enum_rejects_invalid_value() -> None:
    adapter = TypeAdapter(Pair)
    try:
        adapter.validate_python("XAUUSD")
    except ValidationError:
        pass
    else:
        raise AssertionError("Expected invalid pair to raise ValidationError")


def test_other_enums_are_string_serializable() -> None:
    assert PriceBasis.MID == "mid"
    assert EntryTiming.NEXT_BAR_OPEN == "next_bar_open"
    assert PositionMode.NETTING == "netting"
