import pytest

import src.toolkit.errors

from src.toolkit.converter import converter


def test_mass_convert():
    assert converter(12, "kg", "g") == 12000.0


def test_mass_convert_negative():
    with pytest.raises(src.toolkit.errors.WrongValueError):
        converter(-5, "g", "kg")


def test_length_convert():
    assert converter(17, "mm", "cm") == 1.7


def test_length_convert_negative():
    with pytest.raises(src.toolkit.errors.WrongValueError):
        converter(-11, "cm", "km")


def test_temp_convert():
    assert converter(28, "c", "k") == 301.15


def test_temp_convert_negative():
    with pytest.raises(src.toolkit.errors.WrongTemperatureError):
        converter(-274, "c", "k")


def test_incompatible_units():
    with pytest.raises(src.toolkit.errors.IncompatibleUnitsError):
        converter(51, "c", "kg")
