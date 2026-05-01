# pylint: disable=missing-class-docstring, missing-function-docstring
"""
This module contains tests for the Pt class.
"""

import os
import sys
from datetime import datetime

import pytest

FILE_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.realpath(os.path.dirname(FILE_DIR))  # Main folder

os.chdir(FILE_DIR)
sys.path.append(PARENT_DIR + "/ezgpx")

from ezgpx import (  # pylint: disable=wrong-import-position
    Latitude,
    Longitude,
    Pt,
)


class TestPt:

    @pytest.mark.parametrize(
        "lat, lon, ele, time, tag",
        [
            pytest.param(
                Latitude(0),
                Longitude(1),
                3.0,
                datetime(2000, 1, 1),
                "t",
                id="valid",
            ),
        ],
    )
    def test_valid_values(self, lat, lon, ele, time, tag):
        p = Pt(lat, lon, ele, time, tag)
        assert isinstance(p.lat, Latitude)
        assert isinstance(p.lon, Longitude)
        assert isinstance(p.ele, float)
        assert isinstance(p.time, datetime)
        assert isinstance(p.tag, str)
        assert p.lat.value == 0
        assert p.lon.value == 1
        assert p.ele == 3.0
        assert p.time == datetime(2000, 1, 1)
        assert p.tag == "t"

    @pytest.mark.parametrize(
        "lat, lon, ele, time, tag",
        [
            pytest.param(
                "a",
                Longitude(1),
                3.0,
                datetime(2000, 1, 1),
                "t",
                id="not_latitude",
            ),
            pytest.param(
                Latitude(0),
                "a",
                3.0,
                datetime(2000, 1, 1),
                "t",
                id="not_longitude",
            ),
            pytest.param(
                Latitude(0),
                Longitude(1),
                3.0,
                "a",
                "t",
                id="not_datetime",
            ),
        ],
    )
    def test_invalid_values_raise(self, lat, lon, ele, time, tag):
        with pytest.raises(TypeError):
            Pt(lat, lon, ele, time, tag)

    def test_default_values(self):
        m = Pt(lat=Latitude(0), lon=Longitude(1))
        assert m.ele is None
        assert m.time is None
        assert m.tag == "pt"

    def test_fields(self):
        assert Pt._fields == ["lat", "lon", "ele", "time"]

    def test_mandatory_fields(self):
        assert Pt._mandatory_fields == ["lat", "lon"]
