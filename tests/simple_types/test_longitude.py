# pylint: disable=missing-class-docstring, missing-function-docstring
"""
This module contains tests for the Longitude class.
"""

import os
import sys

import pytest

FILE_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.realpath(os.path.dirname(FILE_DIR))  # Main folder

os.chdir(FILE_DIR)
sys.path.append(PARENT_DIR + "/ezgpx")

from ezgpx import Longitude  # pylint: disable=wrong-import-position


class TestLongitude:

    @pytest.mark.parametrize(
        "value, expected",
        [
            pytest.param(0, 0, id="int"),
            pytest.param(0.0, 0, id="float"),
            pytest.param("0.0", 0, id="str"),
        ],
    )
    def test_valid_values(self, value, expected):
        l = Longitude(value)
        assert isinstance(l.value, float)
        assert l.value == expected

    @pytest.mark.parametrize(
        "value",
        [
            pytest.param(-181, id="too_small"),
            pytest.param(-180.0001, id="too_small"),
            pytest.param(180, id="too_big"),
            pytest.param(180.0001, id="too_big"),
        ],
    )
    def test_out_of_range_values_raise(self, value):
        with pytest.raises(ValueError):
            Longitude(value)

    @pytest.mark.parametrize(
        "value",
        [
            pytest.param(None, id="none"),
            pytest.param("a", id="str"),
            pytest.param([], id="list"),
        ],
    )
    def test_invalid_values_raise(self, value):
        with pytest.raises(TypeError):
            Longitude(value)

    def test_lower_boundary_inclusive(self):
        assert Longitude(-180).value == -180

    def test_upper_boundary_exclusive(self):
        with pytest.raises(ValueError):
            Longitude(180)

    def test_float_conversion_preserves_value(self):
        assert Longitude(42).value == 42.0

    def test_repr_contains_value(self):
        d = Longitude(42.0)
        assert "42.0" in repr(d)

    @pytest.mark.parametrize(
        "value_1, value_2, expected",
        [
            pytest.param(0, 1, True),
            pytest.param(1, 0, False),
            pytest.param(0, 0, False),
        ],
    )
    def test_lt(self, value_1, value_2, expected):
        assert (Longitude(value_1) < Longitude(value_2)) == expected

    @pytest.mark.parametrize(
        "value_1, value_2, expected",
        [
            pytest.param(0, 1, False),
            pytest.param(1, 0, True),
            pytest.param(0, 0, False),
        ],
    )
    def test_gt(self, value_1, value_2, expected):
        assert (Longitude(value_1) > Longitude(value_2)) == expected

    @pytest.mark.parametrize(
        "value_1, value_2, expected",
        [
            pytest.param(0, 1, True),
            pytest.param(1, 0, False),
            pytest.param(0, 0, True),
        ],
    )
    def test_le(self, value_1, value_2, expected):
        assert (Longitude(value_1) <= Longitude(value_2)) == expected

    @pytest.mark.parametrize(
        "value_1, value_2, expected",
        [
            pytest.param(0, 1, False),
            pytest.param(1, 0, True),
            pytest.param(0, 0, True),
        ],
    )
    def test_ge(self, value_1, value_2, expected):
        assert (Longitude(value_1) >= Longitude(value_2)) == expected

    @pytest.mark.parametrize(
        "value_1, value_2, expected",
        [
            pytest.param(0, 1, False),
            pytest.param(1, 0, False),
            pytest.param(0, 0, True),
        ],
    )
    def test_eq(self, value_1, value_2, expected):
        assert (Longitude(value_1) == Longitude(value_2)) == expected

    @pytest.mark.parametrize(
        "value_1, value_2, expected",
        [
            pytest.param(0, 1, True),
            pytest.param(1, 0, True),
            pytest.param(0, 0, False),
        ],
    )
    def test_ne(self, value_1, value_2, expected):
        assert (Longitude(value_1) != Longitude(value_2)) == expected
