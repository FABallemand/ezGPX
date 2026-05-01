# pylint: disable=missing-class-docstring, missing-function-docstring
"""
This module contains tests for the DgpsStation class.
"""

import os
import sys

import pytest

FILE_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.realpath(os.path.dirname(FILE_DIR))  # Main folder

os.chdir(FILE_DIR)
sys.path.append(PARENT_DIR + "/ezgpx")

from ezgpx import DgpsStation  # pylint: disable=wrong-import-position


class TestDgpsStation:

    @pytest.mark.parametrize(
        "value, expected",
        [
            pytest.param(0, 0, id="int"),
            pytest.param("0", 0, id="str"),
        ],
    )
    def test_constructor(self, value, expected):
        d = DgpsStation(value)
        assert isinstance(d.value, int)
        assert d.value == expected

    @pytest.mark.parametrize(
        "value",
        [
            pytest.param(-1, id="too_small"),
            pytest.param(1024, id="too_big"),
        ],
    )
    def test_out_of_range_values_raise(self, value):
        with pytest.raises(ValueError):
            DgpsStation(value)

    @pytest.mark.parametrize(
        "value",
        [
            pytest.param(None, id="none"),
            pytest.param(0.0, id="float"),
            pytest.param("a", id="str"),
            pytest.param([], id="list"),
        ],
    )
    def test_invalid_values_raise(self, value):
        with pytest.raises(TypeError):
            DgpsStation(value)

    def test_lower_boundary_inclusive(self):
        assert DgpsStation(0).value == 0

    def test_upper_boundary_inclusive(self):
        assert DgpsStation(1023).value == 1023

    def test_str_conversion_preserves_value(self):
        assert DgpsStation("42").value == 42

    def test_repr_contains_value(self):
        d = DgpsStation(42)
        assert "42" in repr(d)
