# pylint: disable=missing-class-docstring, missing-function-docstring
"""
This module contains tests for the Gpx class.
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
    Gpx,
    Latitude,
    Longitude,
    Metadata,
    Rte,
    Trk,
    Wpt,
)


class TestGpx:

    @pytest.mark.parametrize(
        "version, creator, metadata, wpt, rte, trk, extensions, tag",
        [
            pytest.param(
                "1.1",
                "ezGPX",
                Metadata(),
                [Wpt(Latitude(0), Longitude(1)), Wpt(Latitude(2), Longitude(3))],
                [Rte(), Rte()],
                [Trk(), Trk()],
                Extensions(),
                "t",
                id="valid",
            ),
        ],
    )
    def test_valid_values(
        self, version, creator, metadata, wpt, rte, trk, extensions, tag
    ):
        g = Gpx(version, creator, metadata, wpt, rte, trk, extensions, tag)
        assert isinstance(g.version, str)
        assert isinstance(g.creator, str)
        assert isinstance(g.metadata, Metadata)
        assert isinstance(g.wpt, list)
        assert all(isinstance(w, Wpt) for w in g.wpt)
        assert isinstance(g.rte, list)
        assert all(isinstance(r, Rte) for r in g.rte)
        assert isinstance(g.wpt, list)
        assert all(isinstance(t, Trk) for t in g.trk)
        assert isinstance(g.extensions, Extensions)
        assert isinstance(g.tag, str)
        assert g.version == "1.1"
        assert g.creator == "ezGPX"
        # assert g.metadata == ...
        assert len(g.wpt) == 2
        assert len(g.rte) == 2
        assert len(g.trk) == 2
        # assert g.extensions == ...
        assert g.tag == "t"

    @pytest.mark.parametrize(
        "version, creator, metadata, wpt, rte, trk, extensions, tag",
        [
            pytest.param(
                "1.1",
                "ezGPX",
                42,
                [Wpt(Latitude(0), Longitude(1)), Wpt(Latitude(2), Longitude(3))],
                [Rte(), Rte()],
                [Trk(), Trk()],
                Extensions(),
                "t",
                id="not_metadata",
            ),
            pytest.param(
                "1.1",
                "ezGPX",
                Metadata(),
                42,
                [Rte(), Rte()],
                [Trk(), Trk()],
                Extensions(),
                "t",
                id="not_list_1",
            ),
            pytest.param(
                "1.1",
                "ezGPX",
                Metadata(),
                [42, Wpt(Latitude(2), Longitude(3))],
                [Rte(), Rte()],
                [Trk(), Trk()],
                Extensions(),
                "t",
                id="not_wpt",
            ),
            pytest.param(
                "1.1",
                "ezGPX",
                Metadata(),
                [Wpt(Latitude(0), Longitude(1)), Wpt(Latitude(2), Longitude(3))],
                42,
                [Trk(), Trk()],
                Extensions(),
                "t",
                id="not_list_2",
            ),
            pytest.param(
                "1.1",
                "ezGPX",
                Metadata(),
                [Wpt(Latitude(0), Longitude(1)), Wpt(Latitude(2), Longitude(3))],
                [42, Rte()],
                [Trk(), Trk()],
                Extensions(),
                "t",
                id="not_rte",
            ),
            pytest.param(
                "1.1",
                "ezGPX",
                Metadata(),
                [Wpt(Latitude(0), Longitude(1)), Wpt(Latitude(2), Longitude(3))],
                [Rte(), Rte()],
                42,
                Extensions(),
                "t",
                id="not_list_3",
            ),
            pytest.param(
                "1.1",
                "ezGPX",
                Metadata(),
                [Wpt(Latitude(0), Longitude(1)), Wpt(Latitude(2), Longitude(3))],
                [Rte(), Rte()],
                [42, Trk()],
                Extensions(),
                "t",
                id="not_trk",
            ),
            pytest.param(
                "1.1",
                "ezGPX",
                Metadata(),
                [Wpt(Latitude(0), Longitude(1)), Wpt(Latitude(2), Longitude(3))],
                [Rte(), Rte()],
                [Trk(), Trk()],
                42,
                "t",
                id="not_extensions",
            ),
        ],
    )
    def test_invalid_values_raise(
        self, version, creator, metadata, wpt, rte, trk, extensions, tag
    ):
        with pytest.raises(TypeError):
            Gpx(version, creator, metadata, wpt, rte, trk, extensions, tag)

    def test_default_values(self):
        g = Gpx(version="1.1", creator="ezGPX")
        assert g.metadata is None
        assert g.wpt is None
        assert g.rte is None
        assert g.trk is None
        assert g.tag == "gpx"

    def test_fields(self):
        assert Gpx._fields == [
            "version",
            "creator",
            "metadata",
            "wpt",
            "rte",
            "trk",
            "extensions",
        ]

    def test_mandatory_fields(self):
        assert Gpx._mandatory_fields == ["version", "creator"]
