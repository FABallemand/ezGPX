# pylint: disable=missing-class-docstring, missing-function-docstring
"""
This module contains tests for the Ptseg class.
"""

import os
import sys

import pytest

FILE_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.realpath(os.path.dirname(FILE_DIR))  # Main folder

os.chdir(FILE_DIR)
sys.path.append(PARENT_DIR + "/ezgpx")

from ezgpx import (  # pylint: disable=wrong-import-position
    Latitude,
    Longitude,
    Pt,
    Ptseg,
)


class TestPtseg:

    @pytest.mark.parametrize(
        "pt, tag",
        [
            pytest.param(
                [Pt(Latitude(0), Longitude(1)), Pt(Latitude(2), Longitude(3))],
                "t",
                id="valid",
            ),
        ],
    )
    def test_valid_values(self, pt, tag):
        p = Ptseg(pt, tag)
        assert isinstance(p.pt, list)
        assert all(isinstance(pp, Pt) for pp in p.pt)
        assert isinstance(p.tag, str)
        assert len(p.pt) == 2
        assert p.tag == "t"

    @pytest.mark.parametrize(
        "pt, tag",
        [
            pytest.param(
                42,
                "t",
                id="not_list",
            ),
            pytest.param(
                [42, Pt(Latitude(2), Longitude(3))],
                "t",
                id="not_pt",
            ),
        ],
    )
    def test_invalid_values_raise(self, pt, tag):
        with pytest.raises(TypeError):
            Ptseg(pt, tag)

    def test_default_values(self):
        p = Ptseg()
        assert p.pt is None
        assert p.tag == "ptseg"

    def test_fields(self):
        assert Ptseg._fields == ["pt"]

    def test_mandatory_fields(self):
        assert Ptseg._mandatory_fields == []
