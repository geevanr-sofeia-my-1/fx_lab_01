"""Validation split tests."""

import pytest

from fxlab.validation.splits import make_train_validation_test_split


def test_make_train_validation_test_split_isolated_boundaries() -> None:
    train, validation, test = make_train_validation_test_split(
        list(range(10)),
        train_fraction=0.6,
        validation_fraction=0.2,
        test_fraction=0.2,
    )

    assert train == (train.__class__)(0, 6)
    assert validation == (validation.__class__)(6, 8)
    assert test == (test.__class__)(8, 10)


def test_split_rejects_invalid_fraction_sum() -> None:
    with pytest.raises(ValueError):
        make_train_validation_test_split(
            list(range(10)),
            train_fraction=0.5,
            validation_fraction=0.3,
            test_fraction=0.3,
        )
