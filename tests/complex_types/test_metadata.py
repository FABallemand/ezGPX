# pylint: disable=missing-class-docstring, missing-function-docstring
"""
This module contains tests for the Metadata class.
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
    Bounds,
    Copyright,
    Extensions,
    Link,
    Metadata,
    Person,
)


class TestMetadata:

    @pytest.mark.parametrize(
        "name, desc, author, copyright, link, time, keywords, bounds, extensions, tag",
        [
            pytest.param(
                "test-name",
                "test-desc",
                Person(),
                Copyright("test-author"),
                [Link("test-href-0"), Link("test-href-1"),],
                datetime(2000, 1, 1),
                "test_keywords",
                Bounds(0, 0, 0, 0),
                Extensions(),
                "t",
                id="valid",
            ),
        ],
    )
    def test_valid_values(
        self,
        name,
        desc,
        author,
        copyright,  # pylint: disable=redefined-builtin
        link,
        time,
        keywords,
        bounds,
        extensions,
        tag,
    ):
        m = Metadata(
            name, desc, author, copyright, link, time, keywords, bounds, extensions, tag
        )
        assert isinstance(m.name, str)
        assert isinstance(m.desc, str)
        assert isinstance(m.author, Person)
        assert isinstance(m.copyright, Copyright)
        assert isinstance(m.link, list)
        assert all(isinstance(ll, Link) for ll in m.link)
        assert isinstance(m.time, datetime)
        assert isinstance(m.keywords, str)
        assert isinstance(m.bounds, Bounds)
        assert isinstance(m.extensions, Extensions)
        assert isinstance(m.tag, str)
        assert m.name == "test-name"
        assert m.desc == "test-desc"
        # assert m.author == ...
        # assert m.copyright == ...
        assert len(m.link) == 2
        assert m.time == datetime(2000, 1, 1)
        assert m.keywords == "test_keywords"
        # assert m.bounds == ...
        # assert m.extensions == ...
        assert m.tag == "t"

    @pytest.mark.parametrize(
        "name, desc, author, copyright, link, time, keywords, bounds, extensions, tag",
        [
            pytest.param(
                "test-name",
                "test-desc",
                42,
                Copyright("test-author"),
                [Link("test-href-0"), Link("test-href-1"),],
                datetime(2000, 1, 1),
                "test_keywords",
                Bounds(0, 0, 0, 0),
                Extensions(),
                "t",
                id="not_person",
            ),
            pytest.param(
                "test-name",
                "test-desc",
                Person(),
                42,
                [Link("test-href-0"), Link("test-href-1"),],
                datetime(2000, 1, 1),
                "test_keywords",
                Bounds(0, 0, 0, 0),
                Extensions(),
                "t",
                id="not_copyright",
            ),
            pytest.param(
                "test-name",
                "test-desc",
                Person(),
                Copyright("test-author"),
                42,
                datetime(2000, 1, 1),
                "test_keywords",
                Bounds(0, 0, 0, 0),
                Extensions(),
                "t",
                id="not_list",
            ),
            pytest.param(
                "test-name",
                "test-desc",
                Person(),
                Copyright("test-author"),
                [42, Link("test-href-1"),],
                datetime(2000, 1, 1),
                "test_keywords",
                Bounds(0, 0, 0, 0),
                Extensions(),
                "t",
                id="not_link",
            ),
            pytest.param(
                "test-name",
                "test-desc",
                Person(),
                Copyright("test-author"),
                [Link("test-href-0"), Link("test-href-1"),],
                42,
                "test_keywords",
                Bounds(0, 0, 0, 0),
                Extensions(),
                "t",
                id="not_datetime",
            ),
            pytest.param(
                "test-name",
                "test-desc",
                Person(),
                Copyright("test-author"),
                [Link("test-href-0"), Link("test-href-1"),],
                datetime(2000, 1, 1),
                "test_keywords",
                42,
                Extensions(),
                "t",
                id="not_bounds",
            ),
            pytest.param(
                "test-name",
                "test-desc",
                Person(),
                Copyright("test-author"),
                [Link("test-href-0"), Link("test-href-1"),],
                datetime(2000, 1, 1),
                "test_keywords",
                Bounds(0, 0, 0, 0),
                42,
                "t",
                id="not_extensions",
            ),
        ],
    )
    def test_invalid_values_raise(
        self,
        name,
        desc,
        author,
        copyright,  # pylint: disable=redefined-builtin
        link,
        time,
        keywords,
        bounds,
        extensions,
        tag,
    ):
        with pytest.raises(TypeError):
            Metadata(
                name,
                desc,
                author,
                copyright,
                link,
                time,
                keywords,
                bounds,
                extensions,
                tag,
            )

    def test_default_values(self):
        m = Metadata()
        assert m.name is None
        assert m.desc is None
        assert m.author is None
        assert m.copyright is None
        assert m.link is None
        assert m.time is None
        assert m.keywords is None
        assert m.bounds is None
        assert m.extensions is None
        assert m.tag == "metadata"

    def test_fields(self):
        assert Metadata._fields == [
            "name",
            "desc",
            "author",
            "copyright",
            "link",
            "time",
            "keywords",
            "bounds",
            "extensions",
        ]

    def test_mandatory_fields(self):
        assert Metadata._mandatory_fields == []
