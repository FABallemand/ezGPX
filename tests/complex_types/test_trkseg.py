# pylint: disable=missing-class-docstring, missing-function-docstring
"""
This module contains tests for the Trkseg class.
"""

import os
import sys

import pytest

FILE_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.realpath(os.path.dirname(FILE_DIR))  # Main folder

os.chdir(FILE_DIR)
sys.path.append(PARENT_DIR + "/ezgpx")

from ezgpx import (  # pylint: disable=wrong-import-position
    Extensions,
    Latitude,
    Longitude,
    Trkseg,
    Wpt,
)


class TestTrkseg:

    @pytest.mark.parametrize(
        "trkpt, extensions, tag",
        [
            pytest.param(
                [Wpt(Latitude(0), Longitude(1)), Wpt(Latitude(2), Longitude(3))],
                Extensions(),
                "t",
                id="valid",
            ),
        ],
    )
    def test_valid_values(self, trkpt, extensions, tag):
        t = Trkseg(trkpt, extensions, tag)
        assert isinstance(t.trkpt, list)
        assert all(isinstance(w, Wpt) for w in t.trkpt)
        assert isinstance(t.extensions, Extensions)
        assert isinstance(t.tag, str)
        assert len(t.trkpt) == 2
        # assert t.extensions == ...
        assert t.tag == "t"

    @pytest.mark.parametrize(
        "trkpt, extensions, tag",
        [
            pytest.param(
                42,
                Extensions(),
                "t",
                id="not_list",
            ),
            pytest.param(
                [42, Wpt(Latitude(2), Longitude(3))],
                Extensions(),
                "t",
                id="not_wpt",
            ),
            pytest.param(
                [Wpt(Latitude(0), Longitude(1)), Wpt(Latitude(2), Longitude(3))],
                42,
                "t",
                id="not_extensions",
            ),
        ],
    )
    def test_invalid_values_raise(self, trkpt, extensions, tag):
        with pytest.raises(TypeError):
            Trkseg(trkpt, extensions, tag)

    def test_default_values(self):
        t = Trkseg()
        assert t.trkpt is None
        assert t.extensions is None
        assert t.tag == "trkseg"

    def test_fields(self):
        assert Trkseg._fields == ["trkpt", "extensions"]

    def test_mandatory_fields(self):
        assert Trkseg._mandatory_fields == []
