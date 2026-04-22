# pylint: disable=missing-class-docstring, missing-function-docstring
"""
This module contains tests for the Latitude class.
"""

import os
import sys

import pytest

FILE_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.realpath(os.path.dirname(FILE_DIR))  # Main folder

os.chdir(FILE_DIR)
sys.path.append(PARENT_DIR + "/ezgpx")

from ezgpx import Latitude  # pylint: disable=wrong-import-position


class TestLatitude:

    @pytest.mark.parametrize(
        "value, expected",
        [
            pytest.param(0, 0, id="int"),
            pytest.param(0.0, 0, id="float"),
            pytest.param("0.0", 0, id="str"),
        ],
    )
    def test_valid_values(self, value, expected):
        l = Latitude(value)
        assert l.value == expected
        assert isinstance(l.value, float)

    @pytest.mark.parametrize(
        "value",
        [
            pytest.param(-91, id="too_small"),
            pytest.param(-90.0001, id="too_small"),
            pytest.param(91, id="too_big"),
            pytest.param(91.0001, id="too_big"),
        ],
    )
    def test_out_of_range_values_raise(self, value):
        with pytest.raises(ValueError):
            Latitude(value)

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
            Latitude(value)

    def test_lower_boundary_inclusive(self):
        assert Latitude(-90).value == -90

    def test_upper_boundary_inclusive(self):
        assert Latitude(90).value == 90

    def test_float_conversion_preserves_value(self):
        assert Latitude(42).value == 42.0

    def test_repr_contains_value(self):
        d = Latitude(42.0)
        assert "42.0" in repr(d)
