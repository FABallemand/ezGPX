# pylint: disable=missing-class-docstring, missing-function-docstring
"""
This module contains tests for the Person class.
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
    Email,
    Link,
    Person,
)


class TestPerson:

    @pytest.mark.parametrize(
        "name, email, link, tag",
        [
            pytest.param(
                "test_name",
                Email("test_id", "test_domain"),
                Link("test_href"),
                "t",
                id="valid",
            ),
        ],
    )
    def test_valid_values(self, name, email, link, tag):
        m = Person(name, email, link, tag)
        assert isinstance(m.name, str)
        assert isinstance(m.email, Email)
        assert isinstance(m.link, Link)
        assert isinstance(m.tag, str)
        assert m.name == "test_name"
        # assert m.email == ...
        # assert m.link == ...
        assert m.tag == "t"

    @pytest.mark.parametrize(
        "name, email, link, tag",
        [
            pytest.param(
                "test_name",
                42,
                Link("test_href"),
                "t",
                id="not_email",
            ),
            pytest.param(
                "test_name",
                Email("test_id", "test_domain"),
                42,
                "t",
                id="not_link",
            ),
        ],
    )
    def test_invalid_values_raise(self, name, email, link, tag):
        with pytest.raises(TypeError):
            Person(name, email, link, tag)

    def test_default_values(self):
        m = Person()
        assert m.name is None
        assert m.email is None
        assert m.link is None
        assert m.tag == "person"

    def test_fields(self):
        assert Person._fields == ["name", "email", "link"]

    def test_mandatory_fields(self):
        assert Person._mandatory_fields == []
