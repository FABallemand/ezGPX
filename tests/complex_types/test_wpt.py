# pylint: disable=missing-class-docstring, missing-function-docstring
"""
This module contains tests for the Wpt class.
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
    Degrees,
    DgpsStation,
    Extensions,
    Fix,
    Latitude,
    Link,
    Longitude,
    Wpt,
)


class TestWpt:

    @pytest.mark.parametrize(
        "lat, lon, ele, time, magvar, geoidheight, name, cmt, desc, src, link, sym, type, fix, sat, hdop, vdop, pdop, ageofgpsdata, dgpsid, extensions, tag",
        [
            pytest.param(
                Latitude(0),
                Longitude(1),
                3.0,
                datetime(2000, 1, 1),
                Degrees(0),
                0.0,
                "test_name",
                "test_cmt",
                "test_desc",
                "test_src",
                [Link("test_href_1"), Link("test_href_2")],
                "test_sym",
                "test_type",
                Fix("none"),
                42,
                0.1,
                0.2,
                0.3,
                0.4,
                DgpsStation(0),
                Extensions(),
                "t",
                id="valid",
            ),
        ],
    )
    def test_valid_values(
        self,
        lat,
        lon,
        ele,
        time,
        magvar,
        geoidheight,
        name,
        cmt,
        desc,
        src,
        link,
        sym,
        type,  # pylint: disable=redefined-builtin
        fix,
        sat,
        hdop,
        vdop,
        pdop,
        ageofgpsdata,
        dgpsid,
        extensions,
        tag,
    ):
        w = Wpt(
            lat,
            lon,
            ele,
            time,
            magvar,
            geoidheight,
            name,
            cmt,
            desc,
            src,
            link,
            sym,
            type,
            fix,
            sat,
            hdop,
            vdop,
            pdop,
            ageofgpsdata,
            dgpsid,
            extensions,
            tag,
        )
        assert isinstance(w.lat, Latitude)
        assert isinstance(w.lon, Longitude)
        assert isinstance(w.ele, float)
        assert isinstance(w.time, datetime)
        assert isinstance(w.magvar, Degrees)
        assert isinstance(w.geoidheight, float)
        assert isinstance(w.name, str)
        assert isinstance(w.cmt, str)
        assert isinstance(w.desc, str)
        assert isinstance(w.src, str)
        assert isinstance(w.link, list)
        assert all(isinstance(l, Link) for l in w.link)
        assert isinstance(w.sym, str)
        assert isinstance(w.type, str)
        assert isinstance(w.fix, Fix)
        assert isinstance(w.sat, int)
        assert isinstance(w.hdop, float)
        assert isinstance(w.vdop, float)
        assert isinstance(w.pdop, float)
        assert isinstance(w.ageofgpsdata, float)
        assert isinstance(w.dgpsid, DgpsStation)
        assert isinstance(w.extensions, Extensions)
        assert isinstance(w.tag, str)
        assert w.lat.value == 0
        assert w.lon.value == 1
        assert w.ele == 3.0
        assert w.time == datetime(2000, 1, 1)
        assert w.tag == "t"
        assert w.magvar.value == 0
        assert w.geoidheight == 0.0
        assert w.name == "test_name"
        assert w.cmt == "test_cmt"
        assert w.desc == "test_desc"
        assert w.src == "test_src"
        assert len(w.link) == 2
        assert w.sym == "test_sym"
        assert w.type == "test_type"
        assert w.fix.value == "none"
        assert w.sat == 42
        assert w.hdop == 0.1
        assert w.vdop == 0.2
        assert w.pdop == 0.3
        assert w.ageofgpsdata == 0.4
        assert w.dgpsid.value == 0
        # assert w.extensions == ...
        assert w.tag == "t"

    @pytest.mark.parametrize(
        "lat, lon, ele, time, magvar, geoidheight, name, cmt, desc, src, link, sym, type, fix, sat, hdop, vdop, pdop, ageofgpsdata, dgpsid, extensions, tag",
        [
            pytest.param(
                "a",
                Longitude(1),
                3.0,
                datetime(2000, 1, 1),
                Degrees(0),
                0.0,
                "test_name",
                "test_cmt",
                "test_desc",
                "test_src",
                [Link("test_href_1"), Link("test_href_2")],
                "test_sym",
                "test_type",
                Fix("none"),
                42,
                0.1,
                0.2,
                0.3,
                0.4,
                DgpsStation(0),
                Extensions(),
                "t",
                id="not_latitude",
            ),
            pytest.param(
                Latitude(0),
                "a",
                3.0,
                datetime(2000, 1, 1),
                Degrees(0),
                0.0,
                "test_name",
                "test_cmt",
                "test_desc",
                "test_src",
                [Link("test_href_1"), Link("test_href_2")],
                "test_sym",
                "test_type",
                Fix("none"),
                42,
                0.1,
                0.2,
                0.3,
                0.4,
                DgpsStation(0),
                Extensions(),
                "t",
                id="not_longitude",
            ),
            pytest.param(
                Latitude(0),
                Longitude(1),
                "a",
                datetime(2000, 1, 1),
                Degrees(0),
                0.0,
                "test_name",
                "test_cmt",
                "test_desc",
                "test_src",
                [Link("test_href_1"), Link("test_href_2")],
                "test_sym",
                "test_type",
                Fix("none"),
                42,
                0.1,
                0.2,
                0.3,
                0.4,
                DgpsStation(0),
                Extensions(),
                "t",
                id="not_float_1",
            ),
            pytest.param(
                Latitude(0),
                Longitude(1),
                3.0,
                42,
                Degrees(0),
                0.0,
                "test_name",
                "test_cmt",
                "test_desc",
                "test_src",
                [Link("test_href_1"), Link("test_href_2")],
                "test_sym",
                "test_type",
                Fix("none"),
                42,
                0.1,
                0.2,
                0.3,
                0.4,
                DgpsStation(0),
                Extensions(),
                "t",
                id="not_datetime",
            ),
            pytest.param(
                Latitude(0),
                Longitude(1),
                3.0,
                datetime(2000, 1, 1),
                "a",
                0.0,
                "test_name",
                "test_cmt",
                "test_desc",
                "test_src",
                [Link("test_href_1"), Link("test_href_2")],
                "test_sym",
                "test_type",
                Fix("none"),
                42,
                0.1,
                0.2,
                0.3,
                0.4,
                DgpsStation(0),
                Extensions(),
                "t",
                id="not_degrees",
            ),
            pytest.param(
                Latitude(0),
                Longitude(1),
                3.0,
                datetime(2000, 1, 1),
                Degrees(0),
                "a",
                "test_name",
                "test_cmt",
                "test_desc",
                "test_src",
                [Link("test_href_1"), Link("test_href_2")],
                "test_sym",
                "test_type",
                Fix("none"),
                42,
                0.1,
                0.2,
                0.3,
                0.4,
                DgpsStation(0),
                Extensions(),
                "t",
                id="not_float_2",
            ),
            pytest.param(
                Latitude(0),
                Longitude(1),
                3.0,
                datetime(2000, 1, 1),
                Degrees(0),
                0.0,
                "test_name",
                "test_cmt",
                "test_desc",
                "test_src",
                42,
                "test_sym",
                "test_type",
                Fix("none"),
                42,
                0.1,
                0.2,
                0.3,
                0.4,
                DgpsStation(0),
                Extensions(),
                "t",
                id="not_list",
            ),
            pytest.param(
                Latitude(0),
                Longitude(1),
                3.0,
                datetime(2000, 1, 1),
                Degrees(0),
                0.0,
                "test_name",
                "test_cmt",
                "test_desc",
                "test_src",
                [42, Link("test_href_2")],
                "test_sym",
                "test_type",
                Fix("none"),
                42,
                0.1,
                0.2,
                0.3,
                0.4,
                DgpsStation(0),
                Extensions(),
                "t",
                id="not_link",
            ),
            pytest.param(
                Latitude(0),
                Longitude(1),
                3.0,
                datetime(2000, 1, 1),
                Degrees(0),
                0.0,
                "test_name",
                "test_cmt",
                "test_desc",
                "test_src",
                [Link("test_href_1"), Link("test_href_2")],
                "test_sym",
                "test_type",
                "a",
                42,
                0.1,
                0.2,
                0.3,
                0.4,
                DgpsStation(0),
                Extensions(),
                "t",
                id="not_fix",
            ),
            pytest.param(
                Latitude(0),
                Longitude(1),
                3.0,
                datetime(2000, 1, 1),
                Degrees(0),
                0.0,
                "test_name",
                "test_cmt",
                "test_desc",
                "test_src",
                [Link("test_href_1"), Link("test_href_2")],
                "test_sym",
                "test_type",
                Fix("none"),
                "a",
                0.1,
                0.2,
                0.3,
                0.4,
                DgpsStation(0),
                Extensions(),
                "t",
                id="not_int",
            ),
            pytest.param(
                Latitude(0),
                Longitude(1),
                3.0,
                datetime(2000, 1, 1),
                Degrees(0),
                0.0,
                "test_name",
                "test_cmt",
                "test_desc",
                "test_src",
                [Link("test_href_1"), Link("test_href_2")],
                "test_sym",
                "test_type",
                Fix("none"),
                42,
                "a",
                0.2,
                0.3,
                0.4,
                DgpsStation(0),
                Extensions(),
                "t",
                id="not_float_3",
            ),
            pytest.param(
                Latitude(0),
                Longitude(1),
                3.0,
                datetime(2000, 1, 1),
                Degrees(0),
                0.0,
                "test_name",
                "test_cmt",
                "test_desc",
                "test_src",
                [Link("test_href_1"), Link("test_href_2")],
                "test_sym",
                "test_type",
                Fix("none"),
                42,
                0.1,
                "a",
                0.3,
                0.4,
                DgpsStation(0),
                Extensions(),
                "t",
                id="not_float_4",
            ),
            pytest.param(
                Latitude(0),
                Longitude(1),
                3.0,
                datetime(2000, 1, 1),
                Degrees(0),
                0.0,
                "test_name",
                "test_cmt",
                "test_desc",
                "test_src",
                [Link("test_href_1"), Link("test_href_2")],
                "test_sym",
                "test_type",
                Fix("none"),
                42,
                0.1,
                0.2,
                "a",
                0.4,
                DgpsStation(0),
                Extensions(),
                "t",
                id="not_float_5",
            ),
            pytest.param(
                Latitude(0),
                Longitude(1),
                3.0,
                datetime(2000, 1, 1),
                Degrees(0),
                0.0,
                "test_name",
                "test_cmt",
                "test_desc",
                "test_src",
                [Link("test_href_1"), Link("test_href_2")],
                "test_sym",
                "test_type",
                Fix("none"),
                42,
                0.1,
                0.2,
                0.3,
                "a",
                DgpsStation(0),
                Extensions(),
                "t",
                id="not_float_6",
            ),
            pytest.param(
                Latitude(0),
                Longitude(1),
                3.0,
                datetime(2000, 1, 1),
                Degrees(0),
                0.0,
                "test_name",
                "test_cmt",
                "test_desc",
                "test_src",
                [Link("test_href_1"), Link("test_href_2")],
                "test_sym",
                "test_type",
                Fix("none"),
                42,
                0.1,
                0.2,
                0.3,
                0.4,
                "a",
                Extensions(),
                "t",
                id="not_dgpsstation",
            ),
            pytest.param(
                Latitude(0),
                Longitude(1),
                3.0,
                datetime(2000, 1, 1),
                Degrees(0),
                0.0,
                "test_name",
                "test_cmt",
                "test_desc",
                "test_src",
                [Link("test_href_1"), Link("test_href_2")],
                "test_sym",
                "test_type",
                Fix("none"),
                42,
                0.1,
                0.2,
                0.3,
                0.4,
                DgpsStation(0),
                42,
                "t",
                id="not_extensions",
            ),
        ],
    )
    def test_invalid_values_raise(
        self,
        lat,
        lon,
        ele,
        time,
        magvar,
        geoidheight,
        name,
        cmt,
        desc,
        src,
        link,
        sym,
        type,  # pylint: disable=redefined-builtin
        fix,
        sat,
        hdop,
        vdop,
        pdop,
        ageofgpsdata,
        dgpsid,
        extensions,
        tag,
    ):
        with pytest.raises((TypeError, ValueError)):
            Wpt(
                lat,
                lon,
                ele,
                time,
                magvar,
                geoidheight,
                name,
                cmt,
                desc,
                src,
                link,
                sym,
                type,
                fix,
                sat,
                hdop,
                vdop,
                pdop,
                ageofgpsdata,
                dgpsid,
                extensions,
                tag,
            )

    def test_default_values(self):
        w = Wpt(lat=Latitude(0), lon=Longitude(1))
        assert w.ele is None
        assert w.time is None
        assert w.magvar is None
        assert w.geoidheight is None
        assert w.name is None
        assert w.cmt is None
        assert w.desc is None
        assert w.src is None
        assert w.link is None
        assert w.sym is None
        assert w.type is None
        assert w.fix is None
        assert w.sat is None
        assert w.hdop is None
        assert w.vdop is None
        assert w.pdop is None
        assert w.ageofgpsdata is None
        assert w.dgpsid is None
        assert w.extensions is None
        assert w.tag == "wpt"

    def test_fields(self):
        assert Wpt._fields == [
            "lat",
            "lon",
            "ele",
            "time",
            "magvar",
            "geoidheight",
            "name",
            "cmt",
            "desc",
            "src",
            "link",
            "sym",
            "type",
            "fix",
            "sat",
            "hdop",
            "vdop",
            "pdop",
            "ageofgpsdata",
            "dgpsid",
            "extensions",
        ]

    def test_mandatory_fields(self):
        assert Wpt._mandatory_fields == ["lat", "lon"]
