"""Session labeling tests."""

from datetime import UTC, datetime

import pytest

from fxlab.data.sessions.labels import label_sessions


def test_session_labels_boundary_behavior() -> None:
    asia = label_sessions(datetime(2024, 1, 1, 7, tzinfo=UTC))
    london = label_sessions(datetime(2024, 1, 1, 8, tzinfo=UTC))
    overlap = label_sessions(datetime(2024, 1, 1, 13, tzinfo=UTC))

    assert asia.asia is True
    assert asia.london is False
    assert london.london is True
    assert overlap.london is True
    assert overlap.newyork is True


def test_session_labels_require_timezone_aware_timestamp() -> None:
    with pytest.raises(ValueError):
        label_sessions(datetime(2024, 1, 1, 8))
