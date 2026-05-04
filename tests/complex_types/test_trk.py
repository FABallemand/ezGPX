# pylint: disable=missing-class-docstring, missing-function-docstring
"""
This module contains tests for the Trk class.
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
    Link,
    Trk,
    Trkseg,
)


class TestTrk:

    @pytest.mark.parametrize(
        "name, cmt, desc, src, link, number, type, extensions, trkseg, tag",
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
                [Trkseg(), Trkseg()],
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
        trkseg,
        tag,
    ):
        t = Trk(name, cmt, desc, src, link, number, type, extensions, trkseg, tag)
        assert isinstance(t.name, str)
        assert isinstance(t.cmt, str)
        assert isinstance(t.desc, str)
        assert isinstance(t.src, str)
        assert isinstance(t.link, list)
        assert all(isinstance(ll, Link) for ll in t.link)
        assert isinstance(t.number, int)
        assert isinstance(t.type, str)
        assert isinstance(t.extensions, Extensions)
        assert isinstance(t.trkseg, list)
        assert all(isinstance(tt, Trkseg) for tt in t.trkseg)
        assert isinstance(t.tag, str)
        assert t.name == "test-name"
        assert t.cmt == "test-cmt"
        assert t.desc == "test-desc"
        assert t.src == "test-src"
        assert len(t.link) == 2
        assert t.number == 42
        assert t.type == "test-type"
        # assert t.extensions == ...
        assert len(t.trkseg) == 2
        assert t.tag == "t"

    @pytest.mark.parametrize(
        "name, cmt, desc, src, link, number, type, extensions, trkseg, tag",
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
                [Trkseg(), Trkseg()],
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
                [Trkseg(), Trkseg()],
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
                [Trkseg(), Trkseg()],
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
                [Trkseg(), Trkseg()],
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
                [42, Trkseg()],
                "t",
                id="not_trkseg",
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
        trkseg,
        tag,
    ):
        with pytest.raises((TypeError, ValueError)):
            Trk(name, cmt, desc, src, link, number, type, extensions, trkseg, tag)

    def test_default_values(self):
        r = Trk()
        assert r.name is None
        assert r.cmt is None
        assert r.desc is None
        assert r.src is None
        assert r.link is None
        assert r.number is None
        assert r.type is None
        assert r.extensions is None
        assert r.trkseg is None
        assert r.tag == "trk"

    def test_fields(self):
        assert Trk._fields == [
            "name",
            "cmt",
            "desc",
            "src",
            "link",
            "number",
            "type",
            "extensions",
            "trkseg",
        ]

    def test_mandatory_fields(self):
        assert Trk._mandatory_fields == []
