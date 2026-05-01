# pylint: disable=missing-class-docstring, missing-function-docstring
"""
This module contains tests for the Bounds class.
"""

import os
import sys

import pytest

FILE_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.realpath(os.path.dirname(FILE_DIR))  # Main folder

os.chdir(FILE_DIR)
sys.path.append(PARENT_DIR + "/ezgpx")

from ezgpx import Bounds, Latitude, Longitude  # pylint: disable=wrong-import-position


class TestBounds:

    @pytest.mark.parametrize(
        "minlat, minlon, maxlat, maxlon, tag",
        [
            pytest.param(0, 1, 2, 3, "t", id="int"),
            pytest.param(0.0, 1.0, 2.0, 3.0, "t", id="float"),
            pytest.param("0.0", "1.0", "2.0", "3.0", "t", id="str"),
        ],
    )
    def test_valid_values(self, minlat, minlon, maxlat, maxlon, tag):
        b = Bounds(minlat, minlon, maxlat, maxlon, tag)
        assert isinstance(b.minlat, Latitude)
        assert isinstance(b.minlon, Longitude)
        assert isinstance(b.maxlat, Latitude)
        assert isinstance(b.maxlon, Longitude)
        assert isinstance(b.tag, str)
        assert b.minlat.value == 0
        assert b.minlon.value == 1
        assert b.maxlat.value == 2
        assert b.maxlon.value == 3
        assert b.tag == "t"

    @pytest.mark.parametrize(
        "minlat, minlon, maxlat, maxlon, tag",
        [
            pytest.param(None, 1, 2, 3, "t", id="none"),
            pytest.param("a", 1, 2, 3, "t", id="str"),
            pytest.param([], 1, 2, 3, "t", id="list"),
        ],
    )
    def test_invalid_values_raise(self, minlat, minlon, maxlat, maxlon, tag):
        with pytest.raises(TypeError):
            Bounds(minlat, minlon, maxlat, maxlon, tag)

    def test_default_tag(self):
        b = Bounds(
            minlat=Latitude(0),
            minlon=Longitude(0),
            maxlat=Latitude(1),
            maxlon=Longitude(1),
        )
        assert b.tag == "bounds"

    def test_fields(self):
        assert Bounds._fields == ["minlat", "minlon", "maxlat", "maxlon"]

    def test_mandatory_fields(self):
        assert Bounds._mandatory_fields == ["minlat", "minlon", "maxlat", "maxlon"]
