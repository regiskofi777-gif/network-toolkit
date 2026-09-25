"""Tests de validation """

from network_toolkit.validation import validate_port_range


def test_valid_range():
    validate_port_range(1, 100)


def test_invalid_range_reversed():
    import pytest
    with pytest.raises(SystemExit):
        validate_port_range(100, 1)


def test_invalid_range_out_of_bounds():
    import pytest
    with pytest.raises(SystemExit):
        validate_port_range(0, 100)