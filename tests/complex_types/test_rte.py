# pylint: disable=missing-class-docstring, missing-function-docstring
"""
This module contains tests for the Rte class.
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
    Link,
    Longitude,
    Rte,
    Wpt,
)


class TestRte:

    @pytest.mark.parametrize(
        "name, cmt, desc, src, link, number, type, extensions, rtept, tag",
        [
            pytest.param(
                "test-name",
                "test-cmt",
                "test-desc",
                "test-src",
                [Link("test-href-1"), Link("test-href-2")],
                42,
                "test-type",
                Extensions(),
                [Wpt(Latitude(0), Longitude(1)), Wpt(Latitude(2), Longitude(3))],
                "t",
                id="valid",
            ),
        ],
    )
    def test_valid_values(
        self,
        name,
        cmt,
        desc,
        src,
        link,
        number,
        type,  # pylint: disable=redefined-builtin
        extensions,
        rtept,
        tag,
    ):
        r = Rte(name, cmt, desc, src, link, number, type, extensions, rtept, tag)
        assert isinstance(r.name, str)
        assert isinstance(r.cmt, str)
        assert isinstance(r.desc, str)
        assert isinstance(r.src, str)
        assert isinstance(r.link, list)
        assert all(isinstance(ll, Link) for ll in r.link)
        assert isinstance(r.number, int)
        assert isinstance(r.type, str)
        assert isinstance(r.extensions, Extensions)
        assert isinstance(r.rtept, list)
        assert all(isinstance(w, Wpt) for w in r.rtept)
        assert isinstance(r.tag, str)
        assert r.name == "test-name"
        assert r.cmt == "test-cmt"
        assert r.desc == "test-desc"
        assert r.src == "test-src"
        assert len(r.link) == 2
        assert r.number == 42
        assert r.type == "test-type"
        # assert r.extensions == ...
        assert len(r.rtept) == 2
        assert r.tag == "t"

    @pytest.mark.parametrize(
        "name, cmt, desc, src, link, number, type, extensions, rtept, tag",
        [
            pytest.param(
                "test-name",
                "test-cmt",
                "test-desc",
                "test-src",
                42,
                42,
                "test-type",
                Extensions(),
                [Wpt(Latitude(0), Longitude(1)), Wpt(Latitude(2), Longitude(3))],
                "t",
                id="not_list_1",
            ),
            pytest.param(
                "test-name",
                "test-cmt",
                "test-desc",
                "test-src",
                [42, Link("test-href-2")],
                42,
                "test-type",
                Extensions(),
                [Wpt(Latitude(0), Longitude(1)), Wpt(Latitude(2), Longitude(3))],
                "t",
                id="not_link",
            ),
            pytest.param(
                "test-name",
                "test-cmt",
                "test-desc",
                "test-src",
                [Link("test-href-1"), Link("test-href-2")],
                "a",
                "test-type",
                Extensions(),
                [Wpt(Latitude(0), Longitude(1)), Wpt(Latitude(2), Longitude(3))],
                "t",
                id="not_int",
            ),
            pytest.param(
                "test-name",
                "test-cmt",
                "test-desc",
                "test-src",
                [Link("test-href-1"), Link("test-href-2")],
                42,
                "test-type",
                42,
                [Wpt(Latitude(0), Longitude(1)), Wpt(Latitude(2), Longitude(3))],
                "t",
                id="not_extensions",
            ),
            pytest.param(
                "test-name",
                "test-cmt",
                "test-desc",
                "test-src",
                [Link("test-href-1"), Link("test-href-2")],
                42,
                "test-type",
                Extensions(),
                42,
                "t",
                id="not_list_2",
            ),
            pytest.param(
                "test-name",
                "test-cmt",
                "test-desc",
                "test-src",
                [Link("test-href-1"), Link("test-href-2")],
                42,
                "test-type",
                Extensions(),
                [42, Wpt(Latitude(2), Longitude(3))],
                "t",
                id="not_wpt",
            ),
        ],
    )
    def test_invalid_values_raise(
        self,
        name,
        cmt,
        desc,
        src,
        link,
        number,
        type,  # pylint: disable=redefined-builtin
        extensions,
        rtept,
        tag,
    ):
        with pytest.raises((TypeError, ValueError)):
            Rte(name, cmt, desc, src, link, number, type, extensions, rtept, tag)

    def test_default_values(self):
        r = Rte()
        assert r.name is None
        assert r.cmt is None
        assert r.desc is None
        assert r.src is None
        assert r.link is None
        assert r.number is None
        assert r.type is None
        assert r.extensions is None
        assert r.rtept is None
        assert r.tag == "rte"

    def test_fields(self):
        assert Rte._fields == [
            "name",
            "cmt",
            "desc",
            "src",
            "link",
            "number",
            "type",
            "extensions",
            "rtept",
        ]

    def test_mandatory_fields(self):
        assert Rte._mandatory_fields == []
