# pylint: disable=missing-class-docstring, missing-function-docstring
"""
This module contains tests for the Fix class.
"""

import os
import sys

import pytest

FILE_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.realpath(os.path.dirname(FILE_DIR))  # Main folder

os.chdir(FILE_DIR)
sys.path.append(PARENT_DIR + "/ezgpx")

from ezgpx import Fix, FixType  # pylint: disable=wrong-import-position


class TestFix:

    @pytest.mark.parametrize(
        "value, expected",
        [
            pytest.param("none", FixType.NONE, id="none_str"),
            pytest.param("2d", FixType.D2, id="2d_str"),
            pytest.param("3d", FixType.D3, id="3d_str"),
            pytest.param("dgps", FixType.DGPS, id="dgps_str"),
            pytest.param("pps", FixType.PPS, id="pps_str"),
            pytest.param(FixType.NONE, FixType.NONE, id="none"),
            pytest.param(FixType.D2, FixType.D2, id="2d"),
            pytest.param(FixType.D3, FixType.D3, id="3d"),
            pytest.param(FixType.DGPS, FixType.DGPS, id="dgps"),
            pytest.param(FixType.PPS, FixType.PPS, id="pps"),
        ],
    )
    def test_valid_values(self, value, expected):
        assert Fix(value).value == expected

    @pytest.mark.parametrize(
        "value, exception",
        [
            pytest.param(None, TypeError, id="none"),
            pytest.param(0, TypeError, id="int"),
            pytest.param(0.0, TypeError, id="float"),
            pytest.param("a", ValueError, id="str"),
            pytest.param([], TypeError, id="list"),
        ],
    )
    def test_invalid_values_raise(self, value, exception):
        with pytest.raises(exception):
            Fix(value)

    def test_enum_identity(self):
        fix = Fix("2d")
        assert fix.value is FixType.D2  # ensures Enum, not raw string

    def test_string_conversion(self):
        fix = Fix("none")
        assert isinstance(fix.value, FixType)

    def test_repr_contains_value(self):
        fix = Fix("3d")
        assert "D3" in repr(fix) or "3d" in repr(fix)
