# pylint: disable=missing-class-docstring, missing-function-docstring
"""
This module contains tests for the Copyright class.
"""

import os
import sys

import pytest

FILE_DIR = os.path.dirname(__file__)
PARENT_DIR = os.path.realpath(os.path.dirname(FILE_DIR))  # Main folder

os.chdir(FILE_DIR)
sys.path.append(PARENT_DIR + "/ezgpx")

from ezgpx import Copyright  # pylint: disable=wrong-import-position


class TestCopyright:

    @pytest.mark.parametrize(
        "author, year, license, tag",
        [
            pytest.param("test-author", 2000, "test-license", "t", id="1"),
        ],
    )
    def test_valid_values(self, author, year, license, tag):  # pylint: disable=redefined-builtin
        c = Copyright(author, year, license, tag)
        assert isinstance(c.author, str)
        assert isinstance(c.year, int)
        assert isinstance(c.license, str)
        assert isinstance(c.tag, str)
        assert c.author == "test-author"
        assert c.year == 2000
        assert c.license == "test-license"
        assert c.tag == "t"

    @pytest.mark.parametrize(
        "author, year, license, tag",
        [
            pytest.param("test-author", "a", "test-license", "t", id="str"),
            pytest.param("test-author", [], "test-license", "t", id="list"),
        ],
    )
    def test_invalid_values_raise(self, author, year, license, tag):  # pylint: disable=redefined-builtin
        with pytest.raises((TypeError, ValueError)):
            Copyright(author, year, license, tag)

    def test_default_values(self):
        c = Copyright(
            author="test-author",
        )
        assert c.year is None
        assert c.license is None
        assert c.tag == "copyright"

    def test_fields(self):
        assert Copyright._fields == ["author", "year", "license"]

    def test_mandatory_fields(self):
        assert Copyright._mandatory_fields == ["author"]
