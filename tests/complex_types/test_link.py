# pylint: disable=missing-class-docstring, missing-function-docstring
"""
This module contains tests for the Link class.
"""

import os
import sys

import pytest

FILE_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.realpath(os.path.dirname(FILE_DIR))  # Main folder

os.chdir(FILE_DIR)
sys.path.append(PARENT_DIR + "/ezgpx")

from ezgpx import Link  # pylint: disable=wrong-import-position


class TestLink:

    @pytest.mark.parametrize(
        "href, text, type, tag",
        [
            pytest.param("test-href", "test-text", "test-type", "t", id="valid"),
        ],
    )
    def test_valid_values(
        self, href, text, type, tag  # pylint: disable=redefined-builtin
    ):
        l = Link(href, text, type, tag)
        assert isinstance(l.href, str)
        assert isinstance(l.text, str)
        assert isinstance(l.type, str)
        assert isinstance(l.tag, str)
        assert l.href == "test-href"
        assert l.text == "test-text"
        assert l.type == "test-type"
        assert l.tag == "t"

    def test_default_values(self):
        l = Link(href="test-href")
        assert l.text is None
        assert l.type is None
        assert l.tag == "link"

    def test_fields(self):
        assert Link._fields == ["href", "text", "type"]

    def test_mandatory_fields(self):
        assert Link._mandatory_fields == ["href"]
